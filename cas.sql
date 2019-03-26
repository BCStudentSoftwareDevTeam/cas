-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 26, 2019 at 07:02 PM
-- Server version: 5.7.25-0ubuntu0.16.04.2
-- PHP Version: 7.0.33-0ubuntu0.16.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cas`
--

-- --------------------------------------------------------

--
-- Table structure for table `term`
--

CREATE TABLE `term` (
  `termCode` int(11) NOT NULL,
  `semester` varchar(255) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `state` int(11) NOT NULL,
  `term_state_id` int(11) DEFAULT NULL,
  `editable` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `term`
--

INSERT INTO `term` (`termCode`, `semester`, `year`, `name`, `state`, `term_state_id`, `editable`) VALUES
(201611, 'Fall', 2016, 'Fall 2016', 6, 6, 0),
(201612, 'Spring', 2016, 'Spring 2017', 6, 6, 0),
(201613, '8 Week Summer', 2017, '8 Week Summer 2017', 6, 6, 0),
(201711, 'Fall', 2017, 'Fall 2017', 6, 6, 0),
(201712, 'Spring', 2017, 'Spring 2018', 6, 6, 0),
(201811, 'Fall', 2018, 'Fall 2018', 6, 6, 0),
(201812, 'Spring', 2019, 'Spring 2019', 6, 6, 0),
(201911, 'Fall', 2019, 'Fall 2019', 4, 4, 0),
(201912, 'Spring', 2020, 'Spring 2020', 1, 1, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `term`
--
ALTER TABLE `term`
  ADD PRIMARY KEY (`termCode`),
  ADD KEY `term_term_state_id` (`term_state_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `term`
--
ALTER TABLE `term`
  ADD CONSTRAINT `term_ibfk_1` FOREIGN KEY (`term_state_id`) REFERENCES `termstates` (`csID`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
