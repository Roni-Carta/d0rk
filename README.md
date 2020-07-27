# d0rk

d0rk is a Python tool used to scrape search engines results.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the packages.

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
d0rk.

Usage:
        dorking.py dork <query> [--pages=K]
        dorking.py dork engine <engine> <query> [--pages=K]

Options:
  -h --help     Show this screen.
  --version     Show version.
```

## Example 

```bash
python3 dorking.py dork engine bing "wikipedia" --pages=5

python3 dorking.py dork engine google "inurl:admin"
```

![](preview/d0rking_preview.gif)


## How to get the creds.json

Follow [this tutorial](https://gspread.readthedocs.io/en/latest/oauth2.html#) to get the creds.json and move it to the root of the project.

## Support

| Search engines	| Support		|
| ------------- 	| ------------- |
| Google  			| No			|
| Qwant  			| No			|
| Youtube  			| Yes			|
| DuckduckGo  		| Yes			|
| Bing  			| Yes			|
| Yandex  			| Yes			|
| Ecosia  			| Yes			|
| Gist  			| Yes			|
| Yahoo  			| Yes			|



## The Google Problem 

We are aware that Google queries do not give any data back. When the first version of the tool was made, the queries worked but apparently they silently fixed it.
But don't worry we will find a bypass and get a proper GOOGLE DORKING !

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
