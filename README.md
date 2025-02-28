# CampusTrade
The Campus Trading Application is designed to facilitate secure and efficient peer-to-peer trading within our institute. Students often resort to second-hand buying and selling of goods using social media platforms, which doesn't facilitate the live status of sale, making it an ineffective way of trading. This system enables students, faculty members and non-teaching staff members to list items for sale, browse available products and initiate and complete transactions on this virtual platform, much like a market. 

## Key Features:
- User Management: Secure registration and login for students and staff, with detailed profiles maintained for all users.
- Product Listings: Users can post items with descriptions, images, and pricing.
- Transactions: Supports both direct payments and credit-based purchases.
- Reviews & Ratings: Buyers can rate and review sellers for credibility.
- Reports & Analytics: Generate reports on user activity, popular product categories, and transaction history.

## Database Schema:
The database consists of 10 tables:
- member - Stores user information
- category - Stores product categories
- product_listing - Stores listed products
- transaction_listing - Stores transaction details
- credit_logs - Maintains users' credit balance
- wishlist - Stores users' saved products
- reviews_ratings - Stores user reviews and ratings
- report_analytics - Stores platform-generated reports
- complaints - Stores user complaints
- searches - Logs user search queries

## Technology Stack:
- Backend: Flask (Python)
- Frontend: React
- Database: MySQL
