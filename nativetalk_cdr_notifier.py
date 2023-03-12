import requests
import time
import datetime


# Listens for call records every 5min and sends update to the involved recipient
def listener():
    print("Hello mfs")
    start = datetime.datetime.now
    unique_ids = []

    headers = {
        "x-auth-token": "mzFxYakJRhZ8e6nEqMnhvLBVsVpFVj",
        "Content-Type": "application/json"
    }

    while (True):
        date = datetime.datetime.now()
        new_cdrs = []

        query = 10
        end_stamp = date - datetime.timedelta(0, 0, 0, 0, 5)
        end_stamp_str = end_stamp.strftime("%Y-%m-%d %H:%M:%S") 
        
        test_end = datetime.datetime(2022, 11, 11,  0, 0, 0)
        test_end_str = test_end.strftime("%Y-%m-%d %H:%M:%S")
        print("test_end", test_end_str)

        print("end_stamp", test_end_str)

        data = {
            "id":"328",
            "token":"R3dmU205YWlFdWp5RmMva0ZqdjZjZz09",
            "object":"cdrs",
            "object_params":"*",
            "object_limit_params":"0," + str(query),
            "object_convert_params":"{\"DATE\":[\"\\u003d\",\"callstart\"],\"CURRENCY\":[\"\\u003d\",\"debit\"]}",
            "object_orderby_params": "callstart ASC",
            "object_where_params": "{\"accountid\":[\"\u003d\",\"328\"], \"end_stamp\":[\"\\u003e\\u003d\",\"" + test_end_str + "\"]}"
        }

        response = requests.post(url="https://dashboard.nativetalk.com.ng/api/objects", json=data, headers=headers)

        info = response.json()

        for i in range(0, query):
            try:
                detail = info[str(i)]
                if detail["uniqueid"] not in unique_ids:
                    unique_ids.append(detail['uniqueid'])
                    new_cdrs.append(detail)
            except KeyError:
                print("done")
                break

        print(new_cdrs)
        print("_-------------------------")
        print("_-------------------------")
        print(unique_ids)

          # wait for 5 minutes
        # time.sleep(300)
        if len(new_cdrs) > 0:
            notify_web_hook(new_cdrs)

        time.sleep(3)
        break
        # print(info["0"]["callstart"] + ": ", end="")
        # print(response.json()["0"]["path"])


def notify_web_hook(cdrs):
    bpms_webhook_url = "https://webhook.site/ec116d98-4258-46ca-9f8c-2caa58c4bf31"
    requests.post(url=bpms_webhook_url, json=cdrs)
    # Send details to bpms webhook


if __name__ == '__main__':
    listener()