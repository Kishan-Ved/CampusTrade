drop database if exists CampusTrade;
CREATE DATABASE CampusTrade;
USE CampusTrade;

CREATE TABLE member (
    Member_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Contact_No VARCHAR(15) NOT NULL UNIQUE,
    Age INT NOT NULL,
    Profile_Image LONGBLOB DEFAULT NULL,
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
-- INSERT INTO member (Name, Email, Password, Contact_No, Age, Profile_Image, Role) VALUES
-- ('Alice Johnson', 'alice@example.com', 'hashedpassword1', '9876543210', 22, load_file('/var/lib/mysql-files/Screenshot from 2025-02-28 19-31-16.png'), 'Student'),
-- ('Bob Smith', 'bob@example.com', 'hashedpassword2', '9876543211', 35, load_file('/var/lib/mysql-files/Screenshot from 2025-02-28 19-31-32.png'), 'Faculty'),
-- ('Charlie Brown', 'charlie@example.com', 'hashedpassword3', '9876543212', 28, load_file('/var/lib/mysql-files/Screenshot from 2025-02-28 19-31-42.png'), 'Staff');

-- Insert categories
-- INSERT INTO category (Category_Name) VALUES
-- ('Electronics'),
-- ('Books'),
-- ('Furniture');

-- Insert products
-- INSERT INTO product_listing (Seller_ID, Title, Description, Price, Category_ID, Condition_, Image_URL) VALUES
-- (1, 'Laptop', 'Used MacBook Pro, 16GB RAM, 512GB SSD', 800.00, 1, 'Used', NULL),
-- (2, 'Python Programming Book', 'Learn Python from scratch', 20.00, 2, 'New', NULL),
-- (3, 'Office Chair', 'Ergonomic office chair with lumbar support', 50.00, 3, 'Used', NULL);

-- Insert transactions
-- INSERT INTO transaction_listing (Buyer_ID, Seller_ID, Product_ID, Payment_Method) VALUES
-- (2, 1, 1, 'Cash'),
-- (3, 2, 2, 'Credit');

-- Insert credit logs
-- INSERT INTO credit_logs (Member_ID, Balance) VALUES
-- (1, 100.00),
-- (2, 200.50),
-- (3, 50.00);

-- Insert wishlist items
-- INSERT INTO wishlist (Member_ID, Product_ID) VALUES
-- (1, 2),
-- (2, 3);

-- Insert reviews and ratings
-- INSERT INTO reviews_ratings (Reviewer_ID, Reviewed_User_ID, Rating, Review_Text) VALUES
-- (1, 2, 5, 'Great experience, highly recommend!'),
-- (3, 1, 4, 'Smooth transaction.');

-- Insert report analytics
-- INSERT INTO report_analytics (Report_Type) VALUES
-- ('Monthly Sales Report'),
-- ('User Activity Report');

-- Insert complaints
-- INSERT INTO complaints (Member_ID, Description, Status) VALUES
-- (1, 'Received a faulty product.', 'Open'),
-- (3, 'Seller was unresponsive.', 'Resolved');

-- Insert searches
-- INSERT INTO searches (Member_ID, Query) VALUES
-- (1, 'Laptop'),
-- (2, 'Office Chair');


-- Insert members
INSERT INTO member (Name, Email, Password, Contact_No, Age, Profile_Image, Role) VALUES
('Alice Johnson', 'alice@example.com', 'hashedpassword1', '9876543210', 22, NULL, 'Student'),
('Bob Smith', 'bob@example.com', 'hashedpassword2', '9876543211', 35, NULL, 'Faculty'),
('Charlie Brown', 'charlie@example.com', 'hashedpassword3', '9876543212', 28, NULL, 'Staff'),
('David Lee', 'david@example.com', 'hashedpassword4', '9876543213', 25, NULL, 'Student'),
('Eva Green', 'eva@example.com', 'hashedpassword5', '9876543214', 32, NULL, 'Faculty'),
('Frank White', 'frank@example.com', 'hashedpassword6', '9876543215', 29, NULL, 'Staff'),
('Grace Adams', 'grace@example.com', 'hashedpassword7', '9876543216', 21, NULL, 'Student'),
('Henry Ford', 'henry@example.com', 'hashedpassword8', '9876543217', 40, NULL, 'Faculty'),
('Ivy Clarke', 'ivy@example.com', 'hashedpassword9', '9876543218', 27, NULL, 'Staff'),
('Jack Wilson', 'jack@example.com', 'hashedpassword10', '9876543219', 23, NULL, 'Student'),
('Kishan Ved', 'kishan@example.com', 'hashedpassword11', '9876543220', 20, NULL, 'Student'),
('Aditya Mehta', 'mehta@example.com', 'hashedpassword12', '9876543221', 20, NULL, 'Student'),
('Pratham Sharda', 'ps@example.com', 'hashedpassword13', '9876543222', 20, NULL, 'Student'),
('Nimitt', 'nimitt@example.com', 'hashedpassword14', '9876543223', 20, NULL, 'Student'),
('Jiya Desai', 'jiya@example.com', 'hashedpassword15', '9876543224', 20, NULL, 'Student');

-- Insert categories (University-relevant)
INSERT INTO category (Category_Name) VALUES
('Electronics'),
('Books'),
('Furniture'),
('Stationery'),
('Bicycles'),
('Course Materials'),
('Musical Instruments'),
('Hostel Essentials'),
('Sports Equipment'),
('Lab Equipment'),
('Clothing'),
('Gadgets & Accessories'),
('Art Supplies'),
('Event Tickets');

-- Insert products (University-specific items)
INSERT INTO product_listing (Seller_ID, Title, Description, Price, Category_ID, Condition_, Image_URL) VALUES
(1, 'Laptop', 'Used MacBook Pro, 16GB RAM, 512GB SSD', 800.00, 1, 'Used', NULL),
(2, 'Python Programming Book', 'Learn Python from scratch', 20.00, 2, 'New', NULL),
(3, 'Study Table', 'Wooden study table with drawer', 50.00, 3, 'Used', NULL),
(4, 'Graphing Calculator', 'Casio FX-991EX, perfect for engineering students', 25.00, 4, 'Used', NULL),
(5, 'Road Bicycle', 'Lightweight cycle, great for campus travel', 150.00, 5, 'Used', NULL),
(6, 'Data Structures Textbook', 'Cormen’s Introduction to Algorithms, well maintained', 30.00, 6, 'Used', NULL),
(7, 'Acoustic Guitar', 'Yamaha Acoustic Guitar, good condition', 120.00, 7, 'Used', NULL),
(8, 'Mattress & Pillow Set', 'Single bed mattress for hostel room', 80.00, 8, 'New', NULL),
(9, 'Football', 'Official size FIFA-approved football', 20.00, 9, 'New', NULL),
(10, 'Lab Coat & Safety Glasses', 'Lab coat with safety glasses set', 40.00, 10, 'New', NULL),
(11, 'Wireless Earbuds', 'Noise-canceling earbuds, brand new', 60.00, 12, 'New', NULL),
(12, 'Mechanical Keyboard', 'RGB backlit mechanical keyboard', 75.00, 1, 'Used', NULL),
(13, 'Paint & Brush Set', 'Acrylic paint set with high-quality brushes', 35.00, 13, 'New', NULL),
(14, 'Gaming Mouse', 'Razer gaming mouse with 16,000 DPI', 40.00, 1, 'Used', NULL),
(15, 'Notebook Bundle', '5 notebooks for college notes', 10.00, 4, 'New', NULL),
(16, 'Microscope', 'Basic student microscope for biology classes', 150.00, 10, 'Used', NULL),
(17, 'Festival Event Tickets', '3 tickets for university festival', 30.00, 14, 'New', NULL),
(18, 'Projector', 'Mini HD projector for presentations', 200.00, 1, 'Used', NULL),
(19, 'Cycle Helmet', 'Brand new helmet for cycling safety', 30.00, 5, 'New', NULL),
(20, 'Smartwatch', 'Fitness tracker smartwatch, good battery life', 90.00, 12, 'Used', NULL),

-- Insert transactions (Sanity checked: Buyer ≠ Seller)
INSERT INTO transaction_listing (Buyer_ID, Seller_ID, Product_ID, Payment_Method) VALUES
(3, 1, 1, 'Cash'),   -- Charlie buys Alice's laptop
(4, 2, 2, 'Credit'), -- David buys Python book from Bob
(5, 3, 3, 'Cash'),   -- Eva buys study table from Charlie
(6, 4, 4, 'Credit'), -- Frank buys calculator from David
(7, 5, 5, 'Cash'),   -- Grace buys bicycle from Eva
(8, 6, 6, 'Credit'), -- Henry buys algorithms book from Frank
(9, 7, 7, 'Cash'),   -- Ivy buys guitar from Grace
(10, 8, 8, 'Credit'),-- Jack buys hostel mattress from Henry
(1, 9, 9, 'Cash'),   -- Alice buys football from Ivy
(2, 10, 10, 'Credit');-- Bob buys lab coat from Jack

-- Insert credit logs
INSERT INTO credit_logs (Member_ID, Balance) VALUES
(1, 50.00),
(2, 120.50),
(3, 30.00),
(4, 200.00),
(5, 350.00),
(6, 75.25),
(7, 180.00),
(8, 500.00),
(9, 600.00),
(10, 250.00);

-- Insert wishlist
INSERT INTO wishlist (Member_ID, Product_ID) VALUES
(1, 6),
(2, 1),
(3, 4),
(4, 5),
(4, 7),
(6, 2),
(7, 9),
(7, 10),
(9, 3),
(10, 8);

-- Insert reviews and ratings
INSERT INTO reviews_ratings (Reviewer_ID, Reviewed_User_ID, Rating, Review_Text) VALUES
(3, 1, 5, 'Great seller! Laptop works perfectly.'),
(4, 2, 4, 'Python book was in great condition, but took a while to arrive.'),
(5, 3, 5, 'Study table was well-maintained.'),
(6, 4, 3, 'Calculator had minor scratches but works fine.'),
(7, 5, 5, 'Bicycle was in excellent shape.'),
(8, 6, 4, 'Algorithms book was useful, some pages marked.'),
(9, 7, 5, 'Guitar was exactly as described.'),
(10, 8, 3, 'Mattress was okay, but slightly overpriced.'),
(1, 9, 4, 'Football was new, but packaging was missing.'),
(2, 10, 5, 'Lab coat was clean and fit perfectly.');

-- Insert report analytics
INSERT INTO report_analytics (Report_Type) VALUES
('Top-Selling Products'),
('Most Active Users'),
('Faculty vs Student Transactions'),
('Highest Rated Sellers'),
('Most Purchased Categories'),
('Trending Course Materials'),
('Payment Method Analysis'),
('Wishlist Trends'),
('Complaint Summary'),
('Monthly Transaction Report');

-- Insert complaints (Realistic issues for university context)
INSERT INTO complaints (Member_ID, Description, Status) VALUES
(1, 'Laptop charger was missing.', 'Open'),
(3, 'Calculator had scratches.', 'Resolved'),
(5, 'Bicycle had a flat tire.', 'Open'),
(7, 'Football was deflated on arrival.', 'Resolved'),
(9, 'Guitar strings were worn out.', 'Open'),
(2, 'Python book took too long to be delivered.', 'Resolved'),
(4, 'Study table drawer was broken.', 'Open'),
(6, 'Lab coat size was incorrect.', 'Resolved'),
(8, 'Mattress had stains.', 'Open'),
(10, 'Seller was unresponsive.', 'Resolved');

-- Insert searches (University-relevant)
INSERT INTO searches (Member_ID, Query) VALUES
(1, 'Used MacBook'),
(2, 'Engineering Books'),
(3, 'Study Table'),
(4, 'Graphing Calculator'),
(5, 'Road Bicycle'),
(6, 'Cormen Algorithms Book'),
(7, 'Acoustic Guitar'),
(8, 'Hostel Mattress'),
(9, 'Football'),
(10, 'Lab Coat');






SELECT p.Product_ID, p.Title, p.Description, p.Price, p.Condition_, c.Category_Name, m.Name AS Seller
FROM product_listing p
JOIN category c ON p.Category_ID = c.Category_ID
JOIN member m ON p.Seller_ID = m.Member_ID;

SELECT t.Transaction_ID, b.Name AS Buyer, s.Name AS Seller, p.Title AS Product, t.Payment_Method, t.Transaction_Date
FROM transaction_listing t
JOIN member b ON t.Buyer_ID = b.Member_ID
JOIN member s ON t.Seller_ID = s.Member_ID
JOIN product_listing p ON t.Product_ID = p.Product_ID;
SHOW VARIABLES LIKE 'secure_file_priv';
SHOW GRANTS FOR CURRENT_USER;
SET GLOBAL local_infile = 1;
select * from member;
