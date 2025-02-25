CREATE DATABASE CampusTrade;
USE CampusTrade;

CREATE TABLE member (
    Member_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Contact_No VARCHAR(15) NOT NULL UNIQUE,
    Age INT NOT NULL,
    Profile_Image VARCHAR(255) DEFAULT NULL,
    Role ENUM('Student', 'Faculty', 'Staff') NOT NULL,
    Registered_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category (
    Category_ID INT PRIMARY KEY AUTO_INCREMENT,
    Category_Name VARCHAR(100) NOT NULL UNIQUE
);



CREATE TABLE product_listing (
    Product_ID INT PRIMARY KEY AUTO_INCREMENT,
    Seller_ID INT NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Category_ID INT NOT NULL,
    Condition_ ENUM('New', 'Used') NOT NULL,
    Image_URL VARCHAR(255) DEFAULT NULL,
    Listed_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Seller_ID) REFERENCES member(Member_ID),
    FOREIGN KEY (Category_ID) REFERENCES category(Category_ID)
);


CREATE TABLE transaction_listing (
    Transaction_ID INT PRIMARY KEY AUTO_INCREMENT,
    Buyer_ID INT NOT NULL,
    Seller_ID INT NOT NULL,
    Product_ID INT NOT NULL,
    Payment_Method ENUM('Cash', 'Credit') NOT NULL,
    Transaction_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Buyer_ID) REFERENCES member(Member_ID),
    FOREIGN KEY (Seller_ID) REFERENCES member(Member_ID),
    FOREIGN KEY (Product_ID) REFERENCES product_listing(Product_ID)
);

CREATE TABLE credit_logs (
    Credit_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT NOT NULL,
    Balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (Member_ID) REFERENCES member(Member_ID)
);


CREATE TABLE wishlist (
    Wishlist_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT NOT NULL,
    Product_ID INT NOT NULL,
    Added_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Member_ID) REFERENCES member(Member_ID),
    FOREIGN KEY (Product_ID) REFERENCES product_listing(Product_ID)
);


CREATE TABLE reviews_ratings (
    Review_ID INT PRIMARY KEY AUTO_INCREMENT,
    Reviewer_ID INT NOT NULL,
    Reviewed_User_ID INT NOT NULL,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Review_Text TEXT,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Reviewer_ID) REFERENCES member(Member_ID),
    FOREIGN KEY (Reviewed_User_ID) REFERENCES member(Member_ID)
);


CREATE TABLE report_analytics (
    Report_ID INT PRIMARY KEY AUTO_INCREMENT,
    Report_Type VARCHAR(100) NOT NULL,
    Generated_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE complaints (
    Complaint_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT NOT NULL,
    Description TEXT NOT NULL,
    Status ENUM('Open', 'Resolved') DEFAULT 'Open',
    Filed_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Member_ID) REFERENCES member(Member_ID)
);


CREATE TABLE searches (
    Search_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT NOT NULL,
    Query VARCHAR(255) NOT NULL,
    Searched_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Member_ID) REFERENCES member(Member_ID)
);

-- Insert members
INSERT INTO member (Name, Email, Password, Contact_No, Age, Profile_Image, Role) VALUES
('Alice Johnson', 'alice@example.com', 'hashedpassword1', '9876543210', 22, NULL, 'Student'),
('Bob Smith', 'bob@example.com', 'hashedpassword2', '9876543211', 35, NULL, 'Faculty'),
('Charlie Brown', 'charlie@example.com', 'hashedpassword3', '9876543212', 28, NULL, 'Staff');

-- Insert categories
INSERT INTO category (Category_Name) VALUES
('Electronics'),
('Books'),
('Furniture');

-- Insert products
INSERT INTO product_listing (Seller_ID, Title, Description, Price, Category_ID, Condition_, Image_URL) VALUES
(1, 'Laptop', 'Used MacBook Pro, 16GB RAM, 512GB SSD', 800.00, 1, 'Used', NULL),
(2, 'Python Programming Book', 'Learn Python from scratch', 20.00, 2, 'New', NULL),
(3, 'Office Chair', 'Ergonomic office chair with lumbar support', 50.00, 3, 'Used', NULL);

-- Insert transactions
INSERT INTO transaction_listing (Buyer_ID, Seller_ID, Product_ID, Payment_Method) VALUES
(2, 1, 1, 'Cash'),
(3, 2, 2, 'Credit');

-- Insert credit logs
INSERT INTO credit_logs (Member_ID, Balance) VALUES
(1, 100.00),
(2, 200.50),
(3, 50.00);

-- Insert wishlist items
INSERT INTO wishlist (Member_ID, Product_ID) VALUES
(1, 2),
(2, 3);

-- Insert reviews and ratings
INSERT INTO reviews_ratings (Reviewer_ID, Reviewed_User_ID, Rating, Review_Text) VALUES
(1, 2, 5, 'Great experience, highly recommend!'),
(3, 1, 4, 'Smooth transaction.');

-- Insert report analytics
INSERT INTO report_analytics (Report_Type) VALUES
('Monthly Sales Report'),
('User Activity Report');

-- Insert complaints
INSERT INTO complaints (Member_ID, Description, Status) VALUES
(1, 'Received a faulty product.', 'Open'),
(3, 'Seller was unresponsive.', 'Resolved');

-- Insert searches
INSERT INTO searches (Member_ID, Query) VALUES
(1, 'Laptop'),
(2, 'Office Chair');

SELECT p.Product_ID, p.Title, p.Description, p.Price, p.Condition_, c.Category_Name, m.Name AS Seller
FROM product_listing p
JOIN category c ON p.Category_ID = c.Category_ID
JOIN member m ON p.Seller_ID = m.Member_ID;

SELECT t.Transaction_ID, b.Name AS Buyer, s.Name AS Seller, p.Title AS Product, t.Payment_Method, t.Transaction_Date
FROM transaction_listing t
JOIN member b ON t.Buyer_ID = b.Member_ID
JOIN member s ON t.Seller_ID = s.Member_ID
JOIN product_listing p ON t.Product_ID = p.Product_ID;


