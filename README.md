Python must be installed before continuing.

Run the following command in the backend folder to start the service
```shell
pip install -r requirements.txt
python main.py
```
Once the server starts running Use postman or any other other tool to send the request

Request Format
```
{
    "movies": [
        {
            "movie_name": "",
            "start_date": "",
            "end_date": ""
        },
        {
            "movie_name": "",
            "start_date": "",
            "end_date": ""
        }
    ]
}
```
Date format-

1. Date should be passed as a string with Day and month separated by space. ex-"09 Jun"
2. Day of the month as a zero-padded decimal. ex- 01, 02, ..., 31
3. Abbreviated month name. ex- Jan, Feb, ..., Dec