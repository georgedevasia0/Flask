-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 03, 2020 at 05:13 PM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.2.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mhs`
--

-- --------------------------------------------------------

--
-- Table structure for table `diagnostics`
--

CREATE TABLE `diagnostics` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `diagnosis` varchar(100) NOT NULL,
  `amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `diagnostics`
--

INSERT INTO `diagnostics` (`id`, `p_id`, `diagnosis`, `amount`) VALUES
(1, 1, 'ECG', 200);

-- --------------------------------------------------------

--
-- Table structure for table `medicine_master`
--

CREATE TABLE `medicine_master` (
  `m_id` int(11) NOT NULL,
  `m_name` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `rate` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `medicine_master`
--

INSERT INTO `medicine_master` (`m_id`, `m_name`, `quantity`, `rate`) VALUES
(4, 'Capsuleo', 10, 500),
(5, 'Niharin', 20, 2000);

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `ssn_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `adm_date` varchar(100) NOT NULL,
  `bed_type` varchar(50) NOT NULL,
  `address` varchar(500) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `ssn_id`, `name`, `age`, `adm_date`, `bed_type`, `address`, `city`, `state`, `status`) VALUES
(1, 'ID75845G', 'Prabhu', 20, '2019-12-20', 'general', 'Flat 11', 'Mangalore', 'kerala', 'Active'),
(2, '5616', 'hjbj', 52, '2020-07-29', 'savings', 'jb', 'savings', 'savings', 'Active'),
(3, '5456', 'gvh', 15, '2020-06-28', 'savings', 'chgc', 'deposit', 'deposit', 'InActive'),
(4, '151', 'gvh', 21, '2020-07-27', 'savings', 'hvj', 'deposit', 'savings', 'Active'),
(7, '15131', 'jvjg', 25, '2020-07-20', 'general', 'hvj', 'kannur', 'Karnataka', 'Active'),
(8, '12132', 'hjghj', 5, '2020-07-13', 'general', 'nvj', 'kannur', 'kerala', 'Active'),
(9, '212', 'ghghg', 12, '2020-06-29', 'general', 'jbkj', 'kannur', 'kerala', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `userstore`
--

CREATE TABLE `userstore` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `stakeholder` varchar(100) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `userstore`
--

INSERT INTO `userstore` (`id`, `username`, `password`, `stakeholder`, `time`) VALUES
(1, 'Akhil', 'Akhil@1234', 'Admission-desk-executive ', '2020-07-02 17:58:48'),
(2, 'Sandra', 'Sandra@1234', 'Pharmacist', '2020-07-02 17:59:24'),
(3, 'Karthik', 'Karthik@1234', ' Diagnostic-services-executive', '2020-07-02 18:00:08');

-- --------------------------------------------------------

--
-- Table structure for table `user_medicines`
--

CREATE TABLE `user_medicines` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `med_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_medicines`
--

INSERT INTO `user_medicines` (`id`, `p_id`, `med_id`, `quantity`) VALUES
(1, 1, 5, 10),
(2, 1, 4, 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diagnostics`
--
ALTER TABLE `diagnostics`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `medicine_master`
--
ALTER TABLE `medicine_master`
  ADD PRIMARY KEY (`m_id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userstore`
--
ALTER TABLE `userstore`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_medicines`
--
ALTER TABLE `user_medicines`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diagnostics`
--
ALTER TABLE `diagnostics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `medicine_master`
--
ALTER TABLE `medicine_master`
  MODIFY `m_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `userstore`
--
ALTER TABLE `userstore`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user_medicines`
--
ALTER TABLE `user_medicines`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
