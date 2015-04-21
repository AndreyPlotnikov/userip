import time
import IPy
from django.db import connections


def check_link(user1, user2):
    """Return True if user1 and user2 are linked"""
    if user1 > user2:
        user1, user2 = user2, user1
    cur = connections['userip'].cursor()
    cur.execute('SELECT match FROM users_link WHERE u1_id=%s AND u2_id=%s', (user1, user2))
    row = cur.fetchall()
    if not row:
        return False
    return row[0][0]


def process_matches(max_items):
    """Ananlyze next bunch of source data and update users_link table"""
    conn = connections['userip']
    cur = conn.cursor()
    # trying to acquire lock
    cur.execute("update locks set acquire=true, ts=current_timestamp "
                "where name='link_proc' and (ts < current_timestamp - interval '10' minute or not acquire) returning *")
    ret = cur.fetchall()
    conn.commit()
    if not ret:
        # another instance has been acquired lock already, exiting..
        return None
    try:
        # trying to determine the next new bunch of data
        cur.execute("select last_user_ip_id from vars limit 1")
        last_user_ip_id = cur.fetchall()[0][0]
        if last_user_ip_id is None:
            first = 0
            last = max_items - 1
        else:
            first = last_user_ip_id + 1
            last = first + max_items - 1
        cur.execute("select max(id) from user_ip")
        max_id = cur.fetchall()[0][0]
        complete = False
        if last > max_id:
            last = max_id
            complete = True
        n_source_rows = last - first + 1
        # main query for matching users by ip
        sql = """select u1.user_id as u1_id, u2.user_id as u2_id, u1.id, l.ips, u1.ip, l.match
        from user_ip u1
        left join user_ip u2 on u1.ip=u2.ip and u1.user_id!=u2.user_id
        left join users_link l on least(u1.user_id, u2.user_id)=l.u1_id and greatest(u1.user_id, u2.user_id)=l.u2_id
        where u1.id between %s and %s and u2.id <= %s;
        """
        cur.execute(sql, (first, last, last))
        links = {}
        count = 0
        for row in iter(cur.fetchone, None):
            count += 1
            id = row[2]
            u1_id = row[0]
            u2_id = row[1]
            # Sorting user ids. In users_link table user1 is always less or equal than user2
            if(u2_id < u1_id):
                u1_id, u2_id = u2_id, u1_id
            ukey = (u1_id, u2_id)
            ips = row[3]
            op = 0
            if ips is None:
                ips = []
                op = 2
            link_info = links.get(ukey)
            if link_info is None:
                link_info = {'ips': [str(ip) for ip in ips], 'op': op, 'match': row[5] or False}
                links[ukey] = link_info
            ip = str(row[4])
            if ip in link_info['ips']:
                continue
            for cur_ip in link_info['ips']:
                if IPy.IP(cur_ip).make_net('255.255.255.0') != IPy.IP(ip).make_net('255.255.255.0'):
                    link_info['match'] = True
            link_info['ips'].append(ip)
            if link_info['op'] != 2:
                link_info['op'] = 1
        num_inserts = 0
        num_updates = 0
        # updating users_link with new data
        try:
            cur.execute("select last_user_ip_id from vars limit 1")
            cur.execute("update vars set last_user_ip_id=%s", (last,))
            for ukey, link_info in links.iteritems():
                if link_info['op'] == 2:
                    cur.execute("insert into users_link values (%s, %s, %s::inet[], %s)",
                    (ukey[0], ukey[1], link_info['ips'], link_info['match']))
                    num_inserts += 1
                elif link_info['op'] == 1:
                    cur.execute("update users_link set ips=%s::inet[], match=%s where u1_id=%s and u2_id=%s",
                        (link_info['ips'], link_info['match'], ukey[0], ukey[1]))
                    num_updates += 1
            conn.commit()
        except:
            conn.rollback()
            raise
    finally:
        # release lock
        cur.execute("update locks set acquire=false where name='link_proc' and acquire=true")
        conn.commit()
    return {
        'complete': complete,
        'num_inserts': num_inserts,
        'num_updates': num_updates,
        'source_rows': n_source_rows
    }
