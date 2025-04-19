
-----Create User table-------------
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each user
    name VARCHAR(255) NOT NULL,             -- Full name of the user
    username VARCHAR(100) NOT NULL UNIQUE,  -- Unique username for login
    password VARCHAR(255) NOT NULL,         -- Password with at least 8 characters, including a special character
    phone_number VARCHAR(20),               -- User's phone number
    email VARCHAR(255) NOT NULL UNIQUE,     -- User's email address (must be unique)
    dietary_preference VARCHAR(50),         -- Dietary preference (e.g., Vegan, Vegetarian, etc.)
    role VARCHAR(50) DEFAULT 'user',        -- Role of the user (default is 'user')
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of record creation
);

-----------------Create Recipes table------------
CREATE TABLE Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each recipe
    name VARCHAR(255) NOT NULL,       -- Name of the recipe
    ingredients TEXT NOT NULL,        -- List or description of ingredients
    steps TEXT NOT NULL,              -- Description of cooking steps
    dietary_condition VARCHAR(100),   -- Dietary tags 
    time_taken INT NOT NULL,          -- Time required to prepare the dish (in minutes)
    youtube_link VARCHAR(2083),       -- Link to a YouTube video 
    user_id INT NOT NULL,             -- Foreign key referencing Users table
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for record creation
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE -- Ensures referential integrity
);

-----Insert users in users table-----------------
INSERT INTO Users (user_id, name, username, password, phone_number, email, dietary_preference, role) VALUES
(1, 'Venkat', 'Venkat', 'Pswrd@1234', '9876543210', 'venkat@tc.com', 'Vegetarian', 'admin'),
(3, 'Amith', 'amith1234', 'Amith@123', '6162626268', 'amith@gmail.com', 'Non-Vegetarian', 'user'),
(7, 'Alexandra Contreras', 'ntoavoco', '#60Le$nuSX', '(856)370-4154x97104', 'ntoavoco@example.com', 'Non-Vegetarian', 'user'),
(8, 'Danny Williamson', 'mnqcstbj', 'Oi@gh3b60l', '927.580.8883x09974', 'mnqcstbj@example.com', 'Vegan', 'user'),
(9, 'John Doyle', 'fyorembp', 'xN6l6Hy@3C', '885.269.6822x87407', 'fyorembp@example.com', 'Not Specific', 'user'),
(10, 'Michael Wilson', 'uyvvnnea', 'sV3mon$Nuc', '001-954-210-2665x8658', 'uyvvnnea@example.com', 'Vegetarian', 'admin'),
(11, 'Brenda Oneill', 'rhtlqdme', 'fl##k^xWAn', '+1-342-230-6245x176', 'rhtlqdme@example.com', 'Not Specific', 'admin'),
(12, 'Scott Martinez', 'ubgozncd', 'bMqWwXUKHW', '+1-964-671-0485x4940', 'ubgozncd@example.com', 'Non-Vegetarian', 'user'),
(13, 'Dawn Smith', 'fixhmmwp', '*rRgSRV1D2', '566.745.2016x312', 'fixhmmwp@example.com', 'Vegan', 'admin'),
(14, 'Andrew Keller', 'qolyqurg', 'MBjLAKR*@2', '+1-512-215-9057x8898', 'qolyqurg@example.com', 'Non-Vegetarian', 'admin'),
(15, 'Courtney Anderson', 'cofzxsow', 'ABpBRsh2nA', '439-883-1673', 'cofzxsow@example.com', 'Vegetarian', 'user'),
(17, 'Samantha Moore', 'gyyoyvea', '3HEHTqS4Al', '847.394.8438x79939', 'gyyoyvea@example.com', 'Vegan', 'admin'),
(18, 'Jennifer Sanford', 'shsdeayv', 'x1^3RWQv$b', '(937)973-9514x920', 'shsdeayv@example.com', 'Vegan', 'admin'),
(19, 'Richard Olson', 'jizketpx', '^^a9K^0hSP', '001-292-383-5581x39768', 'jizketpx@example.com', 'Vegetarian', 'user'),
(20, 'Melissa Wright', 'mrlmcwyf', 'MH4%891B3d', '232.218.6539x0484', 'mrlmcwyf@example.com', 'Non-Vegetarian', 'user'),
(21, 'Brent Higgins', 'cfcaacld', '2C#zw*Hu&6', '(464)713-2708x1755', 'cfcaacld@example.com', 'Non-Vegetarian', 'admin'),
(22, 'Elizabeth Bryant', 'ewoqgzas', 'ZZZZ0X#Dk%', '(352)268-5793', 'ewoqgzas@example.com', 'Vegan', 'admin'),
(23, 'Francisco Smith', 'hsdflerz', 'bKnWq6CHY5', '(410)681-0675x71080', 'hsdflerz@example.com', 'Vegan', 'admin'),
(24, 'Leslie Peterson', 'kkwrbfeq', '8#NLnwr38U', '001-908-993-7796x71126', 'kkwrbfeq@example.com', 'Vegan', 'user'),
(25, 'Timothy Graham', 'eouyjpcd', 'awfKKw&2eo', '(658)865-3373', 'eouyjpcd@example.com', 'Non-Vegetarian', 'admin'),
(26, 'Lori Lopez', 'methctps', 'MJ%Dj8y8B&', '2502918745', 'methctps@example.com', 'Vegan', 'admin'),
(27, 'Gabriel Lawson', 'hzevjjop', 'PeeodYfaw!', '001-428-492-8894', 'hzevjjop@example.com', 'Vegan', 'admin'),
(28, 'Marissa Haynes', 'mkdxasoq', 'HMR6KP&W@X', '(474)478-1663x5865', 'mkdxasoq@example.com', 'Not Specific', 'admin'),
(29, 'Steven Johnson', 'ogjsnzss', 'f$TJ4OWZTi', '(601)810-2530x54130', 'ogjsnzss@example.com', 'Not Specific', 'admin'),
(30, 'Lindsey Thomas', 'zoukphjp', 'cCdM87OGjh', '(298)654-3663x2974', 'zoukphjp@example.com', 'Vegetarian', 'admin'),
(31, 'Taylor Hart', 'wgzkmhyx', 'SbmnO*iUHf', '227.456.2283', 'wgzkmhyx@example.com', 'Not Specific', 'admin'),
(32, 'Mark Delgado', 'xtjnyogp', 'PUs6B6mAD9', '917.796.0844x8897', 'xtjnyogp@example.com', 'Not Specific', 'user'),
(33, 'Melissa Holt', 'nsfpacez', 'vuj0ui8P$c', '(783)297-0127x11006', 'nsfpacez@example.com', 'Not Specific', 'admin'),
(34, 'Kelly Williams', 'cnjdbuuj', '7RrDPTk88v', '(540)740-8068x4713', 'cnjdbuuj@example.com', 'Vegan', 'user'),
(35, 'Adam Gallegos', 'pcpupijz', 'HUckxpqo$!', '880.802.4615x7747', 'pcpupijz@example.com', 'Not Specific', 'user'),
(36, 'Danielle Barrett', 'hylhjqsd', 'q#tRLu4a7w', '001-912-263-5249x859', 'hylhjqsd@example.com', 'Vegetarian', 'user'),
(37, 'Elizabeth Cooper', 'ufquopsa', 'RZlUjknT7z', '208.468.3572', 'ufquopsa@example.com', 'Vegetarian', 'admin'),
(38, 'Andrew Lloyd', 'hlirkaek', 'BOkFNUdn3K', '326-698-3987', 'hlirkaek@example.com', 'Vegan', 'admin'),
(39, 'Samantha Robinson', 'uplsoofd', '5F9Ju60$49', '001-714-444-4556', 'uplsoofd@example.com', 'Non-Vegetarian', 'admin'),
(40, 'Diana Pham', 'plvbpbre', 'LVWO3f%Ph8', '692.666.4955', 'plvbpbre@example.com', 'Non-Vegetarian', 'admin'),
(41, 'James Bradley', 'pzayzabn', 'VEFtC2%Zwo', '556.396.4180', 'pzayzabn@example.com', 'Not Specific', 'admin'),
(42, 'Dawn Esparza', 'spdqlucn', 'hLp1yFCq$s', '001-748-519-9193x737', 'spdqlucn@example.com', 'Vegan', 'admin'),
(43, 'Patricia Smith', 'pat1234', 'Pat@1234', '(214)430-1187x88832', 'owqaxumd@example.com', 'Not Specific', 'admin'),
(44, 'Venkay', 'Venkat Phanindra', 'Pswrd@123', '789456123', 'pasun1v@edu.edu', 'Vegan', 'user'),
(45, 'SrijaVadla', 'vadla4s', 'Instagram8$', '9895062350', 'vadla4s@cmich.edu', 'Vegetarian', 'user'),
(46, 'Shivani', 'shivani', 'Welcome@2024', '989765432', 'polag1s@cmich.edu', 'Vegetarian', 'user'),
(47, 'Sai', 'sai', 'Mommydaddy@143', '9895134307', 'sai@gmail.com', 'Not Specific', 'user'),
(48, 'Sai Tej', 'teja', 'Pswrd@123', '9895134310', 'sai.teja@teja.com', 'Not Specific', 'user'),
(49, 'Sai Chandu', 'chandu', 'Chandu@98', '9895134308', 'saic@gmail.com', 'Vegetarian', 'user'),
(50, 'Test Name', 'test_name', 'Pswrd@123', '7845963102', 'test@test.test', 'Not Specific', 'user'),
(51, 'Jaanu', 'jaanusrija', 'Instagram8$', '9895062350', 'jaanu4s@cmich.edu', 'Vegetarian', 'user'),
(52, 'Sai Chandu', 'saichandu', 'Chandu@98', '9895134392', 'saichandu@gmail.com', 'Not Specific', 'user'),
(53, 'Prash', 'prash4', 'Prassu', '6699667722', 'prash@gmail.com', 'Vegan', 'user'),
(54, 'Prakash', 'prakash123', 'Prakash@123', '6162626265', 'prakash@gmail.com', 'Not Specific', 'user');


----Insert recipes-------------------------
INSERT INTO Recipes (recipe_id, name, ingredients, steps, dietary_condition, time_taken, youtube_link, user_id) VALUES
(1, 'Spaghetti Carbonara', 'Spaghetti, eggs, pancetta, Parmesan cheese, black pepper', '1. Cook pasta. 2. Fry pancetta. 3. Mix eggs and cheese. 4. Combine all ingredients.', 'Non-vegetarian', 30, 'https://youtu.be/carbonara', 1),
(2, 'Vegetable Stir Fry', 'Mixed vegetables, soy sauce, ginger, garlic, sesame oil', '1. Chop vegetables. 2. Heat oil. 3. Stir fry vegetables. 4. Add sauce and seasonings.', 'Vegan', 20, 'https://youtu.be/stirfry', 1),
(3, 'Chicken Tikka Masala', 'Chicken, yogurt, tomato sauce, cream, spices', '1. Marinate chicken. 2. Grill chicken. 3. Prepare sauce. 4. Combine chicken and sauce.', 'Non-vegetarian', 45, 'https://youtu.be/tikkamasala', 1),
(4, 'Quinoa Salad', 'Quinoa, cucumber, tomatoes, feta cheese, olive oil, lemon juice', '1. Cook quinoa. 2. Chop vegetables. 3. Mix ingredients. 4. Add dressing.', 'Vegetarian', 25, 'https://youtu.be/quinoasalad', 1),
(6, 'Mushroom Risotto', 'Arborio rice, mushrooms, onion, white wine, vegetable broth, Parmesan', '1. Sauté mushrooms and onion. 2. Add rice and wine. 3. Gradually add broth. 4. Stir in Parmesan.', 'Vegetarian', 40, 'https://youtu.be/mushroomrisotto', 3),
(7, 'Grilled Salmon', 'Salmon fillet, lemon, dill, olive oil, salt, pepper', '1. Marinate salmon. 2. Preheat grill. 3. Grill salmon. 4. Garnish and serve.', 'Pescatarian', 25, 'https://youtu.be/grilledsalmon', 3),
(8, 'Lentil Soup', 'Lentils, carrots, celery, onion, vegetable broth, spices', '1. Sauté vegetables. 2. Add lentils and broth. 3. Simmer until lentils are tender. 4. Season and serve.', 'Vegan', 35, 'https://youtu.be/lentilsoup', 3),
(9, 'Caesar Salad', 'Romaine lettuce, croutons, Parmesan cheese, Caesar dressing', '1. Wash and chop lettuce. 2. Prepare dressing. 3. Toss ingredients together. 4. Add croutons and cheese.', 'Vegetarian', 15, 'https://youtu.be/caesarsalad', 3),
(11, 'Vegetable Lasagna', 'Lasagna noodles, mixed vegetables, tomato sauce, ricotta cheese, mozzarella', '1. Cook noodles. 2. Prepare vegetable filling. 3. Layer ingredients. 4. Bake until bubbly.', 'Vegetarian', 60, 'https://youtu.be/veglasagna', 45),
(12, 'Shrimp Scampi', 'Shrimp, garlic, white wine, lemon juice, butter, parsley, pasta', '1. Cook pasta. 2. Sauté shrimp and garlic. 3. Add wine and lemon juice. 4. Toss with pasta and garnish.', 'Pescatarian', 25, 'https://youtu.be/shrimpscampi', 45),
(42, 'Egg Rice', 'Egg, rice', 'Cook rice, fry egg and combine.', 'Vegetarian', 30, 'https://www.youtube.com/results?search_query=egg+fried+rice', 47),
(43, 'Test Recipe', 'Test, Recipe', 'Testing my recipe.', 'Vegan', 15, NULL, 50),
(44, 'Test', 'Test ingredients', 'Testing procedure.', 'Gluten-Free', 15, 'test', 3),
(45, 'Taco', 'Tortilla, black beans, mild sauce, cheese, onion, tomato', 'Step 1, Step 2, Step 3, Step 4.', 'Vegetarian', 15, NULL, 3),
(46, 'Tomato Rice', 'Tomato, rice', 'Cook tomato with rice.', 'Non-Vegetarian', 30, NULL, 47),
(47, 'Spring Rolls', 'Cabbage, onion, wraps', 'Mix and wrap ingredients, then fry.', 'Vegetarian', 30, NULL, 54);

-------------------------------------------------------------------------------------------------------------------------



--Below are the all queries associated with our project-----------------
-- Retrieve a user by username and password (for login)
SELECT user_id, username, role FROM Users WHERE username = %s AND password = %s;

-- Retrieve a user's username (for forgot username functionality)
SELECT username FROM Users WHERE name = %s AND email = %s AND phone_number = %s;

-- Reset a user's password
UPDATE Users SET password = %s WHERE username = %s;

-- Check if username or email already exists (for signup validation)
SELECT * FROM Users WHERE username = %s OR email = %s;

-- Retrieve all users for admin management
SELECT * FROM Users;

-- Update a user's role (admin/user)
UPDATE Users SET role = %s WHERE user_id = %s;

-- Delete a user by ID
DELETE FROM Users WHERE user_id = %s;


-- ==========================
-- RECIPE MANAGEMENT
-- ==========================

-- Add a new recipe
INSERT INTO Recipes (name, ingredients, steps, dietary_condition, time_taken, youtube_link, user_id) 
VALUES (%s, %s, %s, %s, %s, %s, %s);

-- Retrieve all recipes
SELECT * FROM Recipes;

-- Search for recipes based on dynamic filters
SELECT * FROM Recipes WHERE (1=1)
  AND (ingredients LIKE %s) -- Ingredient filter
  AND (dietary_condition = %s) -- Dietary condition filter
  AND (time_taken <= %s); -- Time taken filter

-- Retrieve recipes added by a specific user
SELECT * FROM Recipes WHERE user_id = %s;

-- Update an existing recipe
UPDATE Recipes 
SET name = %s, ingredients = %s, steps = %s, dietary_condition = %s, time_taken = %s, youtube_link = %s 
WHERE recipe_id = %s;

-- Delete a recipe by ID
DELETE FROM Recipes WHERE recipe_id = %s;

-- ==========================
-- INSIGHTS AND ANALYTICS
-- ==========================

-- Count total users
SELECT COUNT(*) AS total_users FROM Users;

-- Count total recipes
SELECT COUNT(*) AS total_recipes FROM Recipes;

-- Count recipes by dietary condition
SELECT dietary_condition, COUNT(*) AS recipe_count 
FROM Recipes 
GROUP BY dietary_condition;

-- Count users by dietary preference
SELECT dietary_preference, COUNT(*) AS user_count 
FROM Users 
GROUP BY dietary_preference;

-- Count recipes added by each user
SELECT Users.username AS user_name, COUNT(Recipes.recipe_id) AS recipe_count 
FROM Recipes 
JOIN Users ON Recipes.user_id = Users.user_id 
GROUP BY Users.username;

-- Recipes grouped by time taken
SELECT CASE
    WHEN time_taken = 0 THEN 'Instant'
    WHEN time_taken <= 15 THEN 'Less than 15 min'
    WHEN time_taken <= 30 THEN '15 to 30 min'
    ELSE 'More than 30 min'
END AS time_range, COUNT(*) AS recipe_count 
FROM Recipes 
GROUP BY time_range;



