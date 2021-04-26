from view import app as application
import datetime


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)

timestamp = datetime.datetime.fromtimestamp(1612384200)
print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))