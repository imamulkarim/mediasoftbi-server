## Run the server

Run `run.bat` on the command line


## Project Structure

Main file: `main.py`

The server uses **FastAPI** as the service framework. It uses `GET` and `POST` endpoints to serve data.

Each functionality on the server is structured into its own folder (generally) in the `/engine` folder.


## Testing

Tester file: `tester.py`

Use the tester file to access all of the methods and data in the project for ad-hoc unit testing.


## Database

The database is an `MS SQL Server` instance on Joy Da's computer. The `connection.py` module establishes the connection to the database and provides a **cursor** object to interact with the database. Joy Da's computer must stay powered on for the connection to work.

(The module contains all the details for the connection.)


## Requirements (Summary)

* Get **insights** about sales data
* Create **drill down reporting** on sales data
* Make **predictions** about sales of products by category
* Serve these to a frontend for end users as a **Business Intelligence** application


### Insights

* Categorize database columns according to whether they are data columns or measure columns
* Generate data summary on data columns
* Example: Show totals / averages / peaks (highest, lowest) / sudden spikes, etc.


### Drill down reporting

* Allow users to dynamically select database columns and get visualizations for each column (summary form)
* Create relationships between data and measure columns to create dynamic reports depending on user's column selections
* Allow users to click into each visualization in summary form to get a detailed breakdown with more information


### Predictions

* Allow users to select product categories and generate predictions for future sales of that category of product
* Base predictions of future sales on factors such as:
	* Time of year
	* Time of week
	* Holiday / upcoming holiday season
	* Product type / brand
* Allow the developer to easily customize the prediction factors depending on the customer's requirement


## Work done -vs- To be done

### Done
 - [x] Database connection and fetching the right data
 - [x] Integration and setup of data processing and machine learning libraries
 - [x] Basic Machine Learning model using Decision Tree Regression
 - [x] Easily and quickly customizable parameters for machine learning model
 - [x] Caching big datasets (product names) for fast loading
 - [x] Caching setup for trained models for fast delivery to users
 - [x] Basic setup for insight generation (hardcoded = Total sales summary on *"TotalAmt"* column)
 - [x] Basic reporting without drill down features (hardcoded on several database columns)


### To be done
*(As far as current requirements)*
 - [ ] Create a model based on individual product bar codes (currently based on product category)
 - [ ] Integrate holiday season dates as a parameter into the model
 - [ ] Categorize database columns as data or measure
 - [ ] Use database column categories to automate insight and report generation according to predefined formats (defined in the requirements)
