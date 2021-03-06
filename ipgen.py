import sys
import random
import psycopg2 as dbapi
import psycopg2.extras

psycopg2.extras.register_inet()

def worker(num_records):
    conn = dbapi.connect(database='userip')
    cur = conn.cursor()
    while num_records > 0:
        user_id = random.randrange(1, 100000)
        ip = '{}.{}.{}.{}'.format(random.randint(3, 10), random.randint(50, 70),
                                  random.randint(40, 60), random.randint(20, 30))
        cur.execute('''insert into user_ip (user_id, ip, ts) (select %s, %s, now() where not exists
        (select 1 from user_ip where user_id=%s and ip=%s)) returning user_id''',
            (user_id, ip, user_id, ip))
        if cur.fetchall():
            num_records -= 1
        else:
            print 'S',
    conn.commit()



if __name__ == '__main__':
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 100000
    print n
    worker(n)

