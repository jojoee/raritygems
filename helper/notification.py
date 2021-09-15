import requests
import datetime


def line(line_token: str, txt: str) -> None:
    try:
        url = "https://notify-api.line.me/api/notify"
        header = {
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer %s" % line_token,
        }
        data = {"message": txt}
        requests.post(url, headers=header, data=data)

    except Exception as e:
        now = datetime.datetime.now().replace(microsecond=0)
        msg = f"{now} Error send text line: {e}"
        print(msg)
