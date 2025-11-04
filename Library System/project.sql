-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 03, 2023 at 05:14 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
CREATE TABLE IF NOT EXISTS `books` (
  `sid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `book_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `author` varchar(25) NOT NULL,
  `publisher` varchar(25) NOT NULL,
  `year_of_release` varchar(25) NOT NULL,
  `price` double NOT NULL,
  `availability_status` varchar(25) NOT NULL,
  `type_of_book` varchar(25) NOT NULL,
  `information` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cover_img` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `best_seller` varchar(20) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=7119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`sid`, `id`, `book_title`, `author`, `publisher`, `year_of_release`, `price`, `availability_status`, `type_of_book`, `information`, `cover_img`, `best_seller`) VALUES
(1, 1, 'The Little Prince', 'Antoine de Saint-Exupéry', 'Reynal & Hitchcock', '1943', 55, 'Not Available', 'Kids', 'The Little Prince is a classic novella that tells the story of a young prince who travels from planet to planet in search of understanding and wisdom. Along the way, he meets a variety of characters, including a fox, a snake, and a pilot who has crash-landed in the Sahara desert. Through his encounters and experiences, the prince learns valuable lessons about life, love, and friendship. The book is often regarded as a philosophical allegory and has been translated into numerous languages, becoming one of the most widely read and beloved books in the world.', 'img/The_Little_Prince', 'T'),
(2, 2, 'Little Red Riding Hood', 'Charles Perrault', 'HarperCollins Publishers', '1697 ', 20.5, 'Available', 'Kids', 'Little Red Riding Hood is a traditional fairy tale that tells the story of a young girl who wears a red hooded cloak and goes to visit her grandmother in the forest. On her way, she meets a sly wolf who asks her where she is going and learns of her destination. The wolf then goes to the grandmother\'s house, eats her, and waits for Little Red Riding Hood to arrive. When she does, he tricks her into getting close enough to him so that he can eat her too. However, a hunter arrives in time to save them and kill the wolf. The story is often interpreted as a cautionary tale about the dangers of trusting strangers and not following the advice of parents or elders.', 'img/Little_Red_Riding_Hood', ''),
(3, 3, 'The Diary of Anne Frank', 'Anne Frank', 'Bantam Books', '1952', 60, 'Not Available', 'Novela', 'The Diary of Anne Frank is a diary kept by Anne Frank, a Jewish girl who went into hiding with her family during the Nazi occupation of the Netherlands in World War II. Anne started writing the diary when she was 13 years old and continued to write in it until just a few days before her family was discovered and arrested by the Gestapo. The diary chronicles Anne\'s life in hiding, as well as her thoughts, feelings, and aspirations during a time of extreme persecution and fear. After Anne and her family were arrested, her father Otto Frank, who was the only survivor of the family, published the diary, which has become a classic work of literature and an important historical document. The diary has been translated into many languages and has been adapted for film, stage, and television. It is often read as a testament to the resilience and humanity of the human spirit in the face of adversity.', 'img/The_Diary_of_Anne_Frank', 'T'),
(4, 4, 'The Da Vinci Code', 'Dan Brown', 'Doubleday', '2003', 36, 'Not Available', 'Novela', 'The Da Vinci Code is a thriller novel that follows the story of Robert Langdon, a Harvard symbology professor, who becomes embroiled in a murder investigation at the Louvre Museum in Paris. Langdon and a cryptologist named Sophie Neveu find clues in the works of Leonardo da Vinci that lead them on a quest to uncover a conspiracy that has been kept hidden for centuries. The conspiracy involves the Catholic Church, the Holy Grail, and the true nature of Jesus Christ. The novel explores themes of religion, history, and conspiracy theory, and has been both praised and criticized for its portrayal of these topics. The book became a bestseller and has been translated into numerous languages, and was adapted into a successful film in 2006.', 'img/The_Da_Vinci_Code', 'T'),
(5, 5, 'The Easy Way Out', 'Steven Amsterdam', 'Hogarth ', '2017', 40, 'Available', 'Novela', 'The Easy Way Out is a novel that tells the story of Evan, a nurse who works in a hospital\'s palliative care unit, where he helps terminally ill patients to die. Evan struggles with the ethical and emotional challenges of his job, while also dealing with his own personal issues, including his mother\'s declining health and his complicated relationships with his friends and lovers. The novel explores themes of life, death, morality, and compassion, and has been praised for its sensitive and thought-provoking portrayal of end-of-life care. The book was shortlisted for the Australian Prime Minister\'s Literary Award and has received critical acclaim from reviewers and readers alike.', 'img/The_Easy_Way_Out', ''),
(6, 6, 'One and Only', 'Jenni James', 'StoneHouse Ink', '2015', 30, 'Available', 'Romance', 'One and Only is a young adult romance novel that follows the story of a high school girl named Penelope, who has a crush on her best friend\'s older brother, Jake. Penelope believes that Jake is her one true love, but Jake sees her only as a friend. When Jake\'s girlfriend breaks up with him, Penelope sees her chance to finally win his heart. However, things become complicated when she starts to develop feelings for another boy. The novel explores themes of love, friendship, and self-discovery, and has been praised for its relatable characters and emotional depth.', 'img/One_and_Only', ''),
(7, 7, 'Love Me Harder', 'Rebecca Brooke', 'CreateSpace Independent P', '2016', 35, 'Available', 'Romance', 'Love Me Harder is an adult romance novel that follows the story of a woman named Claire, who has been in love with her best friend, Jack, for years. Jack, however, sees Claire only as a friend and has never expressed any romantic interest in her. When Jack\'s relationship with his girlfriend falls apart, Claire sees her chance to finally make a move on him. The novel explores themes of love, friendship, and the challenges of navigating romantic relationships with people who have been in our lives for a long time. The book has received mixed reviews, with some praising its steamy romance and others criticizing its lack of character development.', 'img/Love_Me_Harder', ''),
(8, 8, 'Sleeping Beauty', 'Charles Perrault', 'Penguin Classics', '2011', 15, 'Available', 'Kids', 'Sleeping Beauty is a classic fairy tale that tells the story of a beautiful princess who is cursed by an evil fairy to prick her finger on a spindle and die on her sixteenth birthday. However, a good fairy intervenes and changes the curse so that the princess will not die, but will instead fall into a deep sleep that will last for a hundred years, until a prince comes to wake her up with a kiss. The story has been adapted in numerous ways over the years, including as a popular Disney animated movie. This edition of the book features an introduction and notes by the translator, Christopher Betts, and is accompanied by the original illustrations by Gustave Doré.', 'img/Sleeping_Beauty', ''),
(9, 9, 'Brave New World', 'Aldous Huxley', 'Harper Perennial Modern C', '2006 ', 15, 'Available', 'Novela', 'Brave New World is a dystopian novel set in a future society that is controlled by technology and advanced scientific techniques. In this world, people are genetically engineered, conditioned to be content with their assigned roles in society, and kept happy by a drug called \"soma.\" The story follows the character of Bernard Marx, an outsider who does not fit into the rigid social hierarchy, and his discovery of a community of \"savages\" who live outside of the controlled world. The book explores themes of individuality, freedom, and the consequences of a society that values happiness over truth. Brave New World has become a classic of science fiction and is widely studied in schools and universities around the world.', 'img/Brave_New_World', ''),
(10, 10, 'Don Quixote', 'Miguel de Cervantes', 'Penguin Classics ', '1605 ', 45, 'Available', 'Novela', 'Don Quixote is a novel that tells the story of a middle-aged Spanish gentleman, Alonso Quixano, who becomes so enamored with the stories of chivalry and adventure that he sets out to become a knight himself. He takes the name Don Quixote and, accompanied by his loyal squire Sancho Panza, sets out on a series of comical and often absurd adventures. Don Quixote\'s delusions and the resulting chaos and confusion make up the bulk of the story. The novel is considered one of the most important works of Spanish literature and has had a significant impact on Western literature as a whole. It is known for its complex characters, satirical tone, and exploration of the nature of reality and fiction.', 'img/Don_Quixote', ''),
(11, 11, 'One Hundred Years of Solitude', 'Gabriel García Márquez', 'Harper Perennial Modern C', '2006 ', 15, 'Available', 'Novela', 'One Hundred Years of Solitude tells the story of the Buendía family over the course of seven generations in the fictional town of Macondo, Colombia. The novel blends magical realism with historical events and explores themes of family, love, power, and the cycle of life and death. The story is narrated in a non-linear fashion and includes a cast of eccentric and memorable characters, such as the patriarch José Arcadio Buendía, the matriarch Úrsula Iguarán, and the prophetic Melquíades. One Hundred Years of Solitude is considered a masterpiece of Latin American literature and has had a significant impact on world literature. It has been translated into numerous languages and has won multiple awards, including the Nobel Prize in Literature for its author, Gabriel García Márquez.', 'img/One_Hundred_Years_of_Soli', ''),
(12, 12, 'The Shadow of the Wind', 'Carlos Ruiz Zafón', 'Penguin Books', '2005 ', 15, 'Not Available', 'Novela', 'The Shadow of the Wind is a historical novel set in Barcelona, Spain, in the aftermath of the Spanish Civil War. The story follows a young boy named Daniel Sempere who discovers a book in a secret library called the Cemetery of Forgotten Books. The book is called The Shadow of the Wind and was written by a mysterious author named Julian Carax. Daniel becomes obsessed with the book and sets out to uncover the truth about the author\'s life and the strange events that have surrounded him. As Daniel delves deeper into Carax\'s past, he becomes entangled in a web of secrets, love, and betrayal that threatens to destroy him and everything he loves. The Shadow of the Wind is a richly layered and suspenseful novel that explores the power of books, the legacy of the past, and the human capacity for love and forgiveness. It has become an international bestseller and has been translated into over 40 languages.', 'img/The_Shadow_of_the_Wind', ''),
(13, 13, 'One Thousand and One Nights', 'Anonymous (Arabian folk t', 'Penguin Classics', '2010', 15, 'Available', 'Novela', 'One Thousand and One Nights is a collection of Middle Eastern and South Asian stories and folk tales compiled in Arabic during the Islamic Golden Age. The tales themselves trace their roots back to ancient and medieval Arabic, Persian, Indian, Egyptian and Mesopotamian folklore and literature.', 'img/One_Thousand_and_One_Nigh', ''),
(14, 14, 'Moby-Dick', 'Herman Melville', 'Harper & Brothers Publish', '1851', 15, 'Available', 'Novela', 'Moby-Dick is a novel that tells the story of a sailor named Ishmael, who joins a whaling voyage led by the obsessive Captain Ahab, who is determined to kill the great white whale that took his leg in a previous encounter. The novel explores themes of obsession, revenge, the nature of evil, and the relationship between humanity and the natural world. With its complex characters, vivid descriptions of life aboard a whaling ship, and philosophical musings, Moby-Dick is considered one of the greatest works of American literature.', 'img/Moby_Dick', ''),
(15, 15, 'Twenty Love Poems and a Song of Despair', 'Pablo Neruda', 'Penguin Books', '2004', 14, 'Available', 'Romance', 'Twenty Love Poems and a Song of Despair is a collection of love poems written by Chilean poet Pablo Neruda. The poems are sensual, passionate, and often melancholic, exploring themes of love, desire, and heartbreak. The book includes Neruda\'s most famous poem, \"Tonight I Can Write the Saddest Lines,\" which has become an iconic work of modern poetry. Published in 1924, the collection has been translated into many languages and is widely regarded as one of Neruda\'s most important works.', 'img/Twenty_Love_Poems_and_a_Song_of_Despair', 'T'),
(16, 16, 'Guess How Much I Love You', 'Sam McBratney', 'Candlewick Press', '1995', 8, 'Available', 'Romance', 'The book tells the story of Little Nutbrown Hare and his father, Big Nutbrown Hare, as they try to outdo each other in expressing their love for one another. The charming illustrations and gentle text make it a beloved classic for children and parents alike.', 'img/Guess_How_Much_I_Love_You', ''),
(17, 17, 'Alices Adventures in Wonderland', 'Lewis Carroll', 'HarperCollins', '1865', 15, 'Available', 'Novela', 'Alice\'s Adventures in Wonderland is a novel about a young girl named Alice who falls down a rabbit hole and finds herself in a strange and surreal world. She meets a host of eccentric and fantastical characters, including the Cheshire Cat, the Mad Hatter, and the Queen of Hearts. The book is a classic of children\'s literature and is known for its vivid imagery, wordplay, and imaginative storytelling.', 'img/Alice\'s_Adventures_in_Wonderland', ''),
(18, 18, 'The Steadfast Tin Soldier', 'Hans Christian Andersen', 'Puffin Books', '1925', 15, 'Available', 'Novela', '\"The Steadfast Tin Soldier\" is a fairy tale about a tin soldier with only one leg and a paper dancer he falls in love with. The soldier is separated from the dancer and goes on a series of adventures before finally reuniting with her, only to face tragedy in the end. The story is known for its themes of love, bravery, and the power of imagination.', 'img/The_Steadfast_Tin_Soldier', 'T'),
(19, 19, 'Harry Potter and the Philosopher Stone', 'J.K. Rowling', 'Scholastic Inc.', '1998', 15, 'Available', 'Novela', 'Harry Potter and the Philosopher\'s Stone is the first book in the Harry Potter series. It follows the story of Harry Potter, a young orphan who discovers on his eleventh birthday that he is a wizard. He is whisked away to Hogwarts School of Witchcraft and Wizardry, where he makes new friends and enemies, and begins to learn about the magical world. However, as he begins to uncover the truth about his parents\' deaths and his own destiny, he must confront the evil wizard, Voldemort, who seeks to destroy him.', 'img/Harry_Potter', ''),
(20, 20, 'Charlie and the Chocolate Factory', 'Roald Dahl', 'Puffin Books', '1964', 15, 'Available', 'Novela', 'Charlie and the Chocolate Factory is a children\'s book that tells the story of a young boy named Charlie Bucket who wins a golden ticket to visit the mysterious Willy Wonka\'s chocolate factory. Once inside, he embarks on a fantastic and magical adventure, meeting a variety of peculiar characters, including the Oompa-Loompas, and ultimately learns a valuable lesson about the importance of kindness and gratitude.', 'img/Charlie_and_the_Chocolate_Factory', ''),
(4904, 0, 'This a new Book', 'New Author', 'New Publisher', 'This year', 100000, 'Available', 'New Book', 'New Information', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `lending_books`
--

DROP TABLE IF EXISTS `lending_books`;
CREATE TABLE IF NOT EXISTS `lending_books` (
  `sid` int NOT NULL AUTO_INCREMENT,
  `id` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `book_title` varchar(750) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(70) NOT NULL,
  `date_of_lending` varchar(25) NOT NULL,
  `date_of_return` varchar(25) NOT NULL,
  `status` varchar(25) NOT NULL,
  `remarks` varchar(25) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lending_books`
--

INSERT INTO `lending_books` (`sid`, `id`, `book_title`, `name`, `date_of_lending`, `date_of_return`, `status`, `remarks`) VALUES
(63, '12', 'The Shadow of the Wind', 'CuestaS', '2023-04-09', '2023-05-05', '', ''),
(57, '3', 'The Diary of Anne Frank', 'Admin', '2023-04-10', '2023-04-27', 'Good ....', 'Good ....'),
(64, '1', 'The Little Prince', 'HernandezI', '2023-04-09', '2023-04-27', '', ''),
(62, '4', 'The Da Vinci Code', 'CuestaS', '2023-04-10', '2023-04-20', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `users_tab`
--

DROP TABLE IF EXISTS `users_tab`;
CREATE TABLE IF NOT EXISTS `users_tab` (
  `sid` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(25) NOT NULL,
  `userid` varchar(25) NOT NULL,
  `password` varchar(25) NOT NULL,
  `role` varchar(25) NOT NULL,
  `my_books` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `books_returned` varchar(50) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=8536 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users_tab`
--

INSERT INTO `users_tab` (`sid`, `user_name`, `userid`, `password`, `role`, `my_books`, `books_returned`) VALUES
(1, 'Isaac', 'admin', 'admin', 'A', ' ,The Diary of Anne Frank ,', ''),
(2, 'Ismael', 'HernandezI', 'ismael', 'U', 'The Little Prince ,', ''),
(3, 'Samara', 'CuestaS', 'samara', 'U', 'The Da Vinci Code ,The Shadow of the Wind ,', ''),
(8535, 'Isaac', 'BautistaI', 'isaac', 'U', '', ''),
(6486, 'Daniela', 'ColmenaresD', 'daniela', 'U', '', '');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
