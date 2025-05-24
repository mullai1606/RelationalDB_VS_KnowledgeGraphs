# RelationalDB_VS_KnowledgeGraphs
Comparing Realational DB and Knowledge gRaph using Flask and SQl and Ne04j

Application Frontend GUI
![image](https://github.com/user-attachments/assets/e7e0d06f-3249-4df9-9208-bb4cf6cc198d)

![image](https://github.com/user-attachments/assets/67ba94ce-ffcb-462c-aad7-29a70e1beba6)

![image](https://github.com/user-attachments/assets/87584140-01f5-4505-80ab-1e604e5a3a15)


**Overview** :

we are Going to Compare  R-DB vs Knowledge Graph by Develop an flask application in two ways 1 with SQL(R-DB) as Backend and the other with Neo4J as backend and the Front end is of HTML and CSS.
The application - Product Management System 
R-DB 
	Entities:
•	Product (id, name, Category, cost, version, decription)
•	SubProduct (id, name, version, belongs_to_product,decription)
•	Supplier (id, name, contact, plant/brand)
•	Plant/brand (id, name, location)
•	Category (id, name, description)
	Relationships:
•	A Product is composed of multiple Sub Products
•	A Supplier produces product and  Sub Product
•	A Plant manages many Products
•	Product belongs to a Category

KG
Nodes (Entities / Classes)
Node Type	Properties
Product	id, name, version, cost, description
SubProduct	id, name, version, description
Category	id, name, description
Supplier	id, name, contact, email
Consumer	id, name, contact, email
Plant (Brand)	id, name, location
Admin	id, password (static values)
Rating	value
Purchase	timestamp

🔗 Edges (Relationships)
Edge (Relation)	From Node	To Node	Meaning
HAS_SUBPRODUCT	Product	SubProduct	A product is composed of sub-products
BELONGS_TO_CATEGORY	Product	Category	Product belongs to a category
BELONGS_TO_CATEGORY	SubProduct	Category	Subproduct inherits product's category
PRODUCES	Supplier	Product	Supplier creates the product
PRODUCES	Supplier	SubProduct	Supplier also creates subproducts
MANAGES_PRODUCT	Plant	Product	Brand manages this product
HAS_BRAND / REGISTERED_BRAND	Supplier	Plant	Supplier is associated with a brand
PURCHASED	Consumer	Product	Consumer bought this product
RATED	Consumer	Rating	Consumer gave a rating
RATING_FOR	Rating	Product	The rating applies to a specific product
IS_SUBPRODUCT_OF (optional inverse)	SubProduct	Product	Inverse of HAS_SUBPRODUCT


for example :
product-"voice conversion ai"(id"automatically generated", name"voice conversion ai", category"AI", cost"10$", version"1.1", description"converting text into voice using prerained voice models")
subProduct - "voice to voice conversion"(id"automatically generated",name"voice to voice conversion", version"1.1", belongs_to_product"voice conversion ai",decription"converting voice into another voice using prerained voice models") 

SQL Tables:
1. User Table
2. Product Table
Application Modules:
1.	Authentication Module 
2.	Product mgmt.
3.	Supplier
4.	Consumer
5.	Admin
6.	DB module
7.	setup
8.	Frontend

Overview:
1.Authentication Module:
•	Handles:
-	Login for all users (Consumer, Supplier, Admin)
-	New user registration (Consumer, Supplier)
•	Key Files:
-	auth_routes.py
-	user_models.py
-	auth_templates/ (HTML pages)

2.Product Management Module
•	Handles:
-	Product and SubProduct creation, editing, deletion
-	Product browsing and viewing (details for both consumer and supplier)
•	Key Files:
-	product_routes.py
-	product_models.py
-	product_templates/ (HTML pages)

3.Supplier Module
•	Handles:
-	Supplier dashboard
-	Managing own products
-	Adding new brand/plant
•	Key Files:
-	supplier_routes.py
-	supplier_templates/ (HTML pages)

4.Consumer Module
Handles:
•	Browsing products
•	Purchasing and rating products
•	Viewing product details
Key Files:
•	consumer_routes.py
•	consumer_templates/ (HTML pages)

5.Admin Module
•	Handles:
-	Admin login
-	Viewing/deleting all products and users
•	Key Files:
-	admin_routes.py
-	admin_templates/ (HTML pages)

6. Database Module
•	Handles:
                    - Models for all entities:
	Product
	 SubProduct
	 Supplier
	 Brand/Plant
	 Category
	 User (Consumer/Supplier/Admin)




7. Main Application Setup
•	Handles:
-	Flask App init
-	DB Config
-	Route registration
•	Key Files:
-	app.py
-	config.py
-	requirements.txt

8. Frontend Module (HTML/CSS)
•	Handles:
-	User interface
-	Navigation and form rendering
•	Key Folders:
-	templates/ (HTML Templates per module)
-	static/
-	css/

MODULE FLOW SUMMARY
•	Auth Module Flow
-	Show login screen
-	Select role (Consumer / Supplier / Create User)
-	On create → role-based form → generate ID → show popup
-	On login → validate → go to respective dashboard
•	Consumer Flow
-	Dashboard: List of products
-	Click product → details page
-	Purchase → Popup + rating → Logout
•	Supplier Flow
-	Dashboard: List of products created
-	Click product → Edit/Delete
-	Add product or subproduct → Fill form → Save
-	Register new brand
•	Admin Flow
-	Admin login (id: admin, pwd: 12345)
-	Dashboard: Lists of users & products
-	Can delete any product/user
