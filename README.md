# webscraper
Webscraper is a Python project that extracts and organizes data from a web site and stores them in json format.

## Installation

Download pip and navigate where the requirements.txt file is inside the command prompt. Then execute the command: pip install -r requirements.txt

## Usage

From the command prompt navigate where the argyle.py file is and run: python argyle.py
A chrome web browser will open.
Enter your credentials to access the web site.
A file called data.json will be automatically created in your working directory.
There is also a version called another_solver.py that tries to enter the credentials automatically and solve the reCapthca if it pops up.

## Docker usage

Docker run command:
docker run -ti argyle

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
