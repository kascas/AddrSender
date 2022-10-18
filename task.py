from time import sleep
import schedule
import addr_sender


def main():
    is_send, count, max_try = False, 0, 60
    while True:
        is_send = addr_sender.check_and_send(on_start=True)
        count += 1
        if is_send:
            break
        if count >= max_try:
            return
        sleep(10)
        print('try:', count)
    schedule.every(60 * 10).seconds.do(addr_sender.check_and_send)
    while True:
        schedule.run_pending()
        sleep(10)

if __name__=='__main__':
    main()