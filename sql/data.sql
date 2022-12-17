INSERT INTO comments(commentid, owner, postid, text)
VALUES (1, 'awdeorio', 3, '#chickensofinstagram');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (2, 'jflinn', 3, 'I <3 chickens');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (3, 'michjc', 3, 'Cute overload!');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (4, 'awdeorio', 2, 'Sick #crossword');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (5, 'jflinn', 1, 'Walking the plank #chickensofinstagram');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (6, 'awdeorio', 1, 'This was after trying to teach them to do a #crossword');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (7, 'jag', 4, 'Saw this on the diag yesterday!');

INSERT INTO following(username1, username2)
VALUES ('awdeorio', 'jflinn');

INSERT INTO following(username1, username2)
VALUES ('awdeorio', 'michjc');

INSERT INTO following(username1, username2)
VALUES ('jflinn', 'awdeorio');

INSERT INTO following(username1, username2)
VALUES ('jflinn', 'michjc');

INSERT INTO following(username1, username2)
VALUES ('michjc', 'awdeorio');

INSERT INTO following(username1, username2)
VALUES ('stschaef', 'awdeorio');

INSERT INTO following(username1, username2)
VALUES ('michjc', 'jag');

INSERT INTO following(username1, username2)
VALUES ('jag', 'michjc');

INSERT INTO likes(owner, postid)
VALUES ('awdeorio', 1);

INSERT INTO likes(owner, postid)
VALUES ('michjc', 1);

INSERT INTO likes(owner, postid)
VALUES ('jflinn', 1);

INSERT INTO likes(owner, postid)
VALUES ('awdeorio', 2);

INSERT INTO likes(owner, postid)
VALUES ('michjc', 2);

INSERT INTO likes(owner, postid)
VALUES ('awdeorio', 3);

INSERT INTO posts(postid, filename, owner)
VALUES (1, '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'awdeorio');

INSERT INTO posts(postid, filename, owner)
VALUES (10, 'nyan.gif', 'awdeorio');

INSERT INTO posts(postid, filename, owner)
VALUES (2, 'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'jflinn');

INSERT INTO posts(postid, filename, owner)
VALUES (3, '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'awdeorio');

INSERT INTO posts(postid, filename, owner)
VALUES (4, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'jag');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('stschaef', 'Steven Schaefer', 'stschaef@umich.edu', 'banane.jpeg', 'kittens');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('awdeorio', 'Andrew DeOrio', 'awdeorio@umich.edu', 'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'sha512$f9b8885dd0de4eb982149607e149a1ac$751b3c28665f2b4dbd1ab746c8fe6e0e9b020f7f8a4a79450fb15c3a1a1bb1f771ac832927279d0ba82508260e71203dddba1cbeb6a9cf5829a820140438bbba');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('jflinn', 'Jason Flinn', 'jflinn@umich.edu', '505083b8b56c97429a728b68f31b0b2a089e5113.jpg', 'sha512$f9b8885dd0de4eb982149607e149a1ac$751b3c28665f2b4dbd1ab746c8fe6e0e9b020f7f8a4a79450fb15c3a1a1bb1f771ac832927279d0ba82508260e71203dddba1cbeb6a9cf5829a820140438bbba');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('michjc', 'Michael Cafarella', 'michjc@umich.edu', '5ecde7677b83304132cb2871516ea50032ff7a4f.jpg', 'sha512$f9b8885dd0de4eb982149607e149a1ac$751b3c28665f2b4dbd1ab746c8fe6e0e9b020f7f8a4a79450fb15c3a1a1bb1f771ac832927279d0ba82508260e71203dddba1cbeb6a9cf5829a820140438bbba');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('jag', 'H.V. Jagadish', 'jag@umich.edu', '73ab33bd357c3fd42292487b825880958c595655.jpg', 'sha512$f9b8885dd0de4eb982149607e149a1ac$751b3c28665f2b4dbd1ab746c8fe6e0e9b020f7f8a4a79450fb15c3a1a1bb1f771ac832927279d0ba82508260e71203dddba1cbeb6a9cf5829a820140438bbba');
