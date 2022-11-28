IF NOT EXISTS ( SELECT * FROM sys.databases WHERE name = 'PriceMatchingSystem' )
BEGIN
    CREATE DATABASE [PriceMatchingSystem]
END
GO

USE [PriceMatchingSystem]
GO

DROP TABLE IF EXISTS [tbl_UserBookmark];
DROP TABLE IF EXISTS [tbl_Login];
DROP TABLE IF EXISTS [tbl_User];
DROP TABLE IF EXISTS [tbl_Admin];
DROP TABLE IF EXISTS [tbl_PriceDetail];
DROP TABLE IF EXISTS [tbl_Source];
DROP TABLE IF EXISTS [tbl_ProductDetail];
DROP TABLE IF EXISTS [tbl_Product];


CREATE TABLE [tbl_User] (
    UserId		INT				NOT NULL IDENTITY,
    UserName	NVARCHAR(50)	NOT NULL,
	FirstName	NVARCHAR(250),
	LastName	NVARCHAR(250),
	Address1	NVARCHAR(50),
	Address2	NVARCHAR(50),
	City		NVARCHAR(250),
	Province	NVARCHAR(50),
	Country		NVARCHAR(250),
	PostalCode	NVARCHAR(20),
	Phone		NVARCHAR(20),
	PhotoURL	NVARCHAR(250)

	CONSTRAINT PK_User PRIMARY KEY(UserId)
)

CREATE TABLE [tbl_Login] (
	LoginId		INT				NOT NULL IDENTITY,
	Email		NVARCHAR(250)	NOT NULL UNIQUE,
	Password	NVARCHAR(MAX)	NOT NULL,
	UserId		INT				NOT NULL

	CONSTRAINT PK_Login PRIMARY KEY(LoginId),
	CONSTRAINT FK_Login_User FOREIGN KEY(UserId) REFERENCES [tbl_User](UserId)
)

CREATE TABLE [tbl_Admin] (
	AdminId		INT				NOT NULL IDENTITY,
	AdminName	NVARCHAR(250)	NOT NULL,
	Password	NVARCHAR(MAX)	NOT NULL

	CONSTRAINT PK_Admin PRIMARY KEY(AdminId),
)

CREATE TABLE [tbl_Product] (
	ProductId	INT				NOT NULL IDENTITY,
	ProductName	NVARCHAR(250)	NOT NULL,

	CONSTRAINT PK_Product PRIMARY KEY(ProductId),
)

CREATE TABLE [tbl_ProductDetail] (
	ProductDetailId		INT				NOT NULL IDENTITY,
	Model				NVARCHAR(250)	NOT NULL,
	Year				INT				NOT NULL,
	Storage				NVARCHAR(250)	NOT NULL,
	ProductId			INT				NOT NULL 

	CONSTRAINT PK_ProductDetail PRIMARY KEY(ProductDetailId),
	CONSTRAINT FK_ProductDetail_Product FOREIGN KEY(ProductId) REFERENCES [tbl_Product](ProductId)
)

CREATE TABLE [tbl_Source] (
	SourceId	INT				NOT NULL IDENTITY,
	SourceName	NVARCHAR(250)	NOT NULL,
	SourceURL	NVARCHAR(250)	NOT NULL,

	CONSTRAINT PK_Source PRIMARY KEY(SourceId)
)

CREATE TABLE [tbl_PriceDetail] (
	PriceDetailId		INT		NOT NULL IDENTITY,
	PriceDetailDate		DATE	NOT NULL,
	Price				MONEY	NOT NULL,
	SourceId			INT		NOT NULL,
	ProductDetailId		INT		NOT NULL

	CONSTRAINT PK_PriceDetail PRIMARY KEY(PriceDetailId),
	CONSTRAINT FK_PriceDetail_Source FOREIGN KEY(SourceId) REFERENCES [tbl_Source](SourceId),
	CONSTRAINT FK_PriceDetail_ProductDetail FOREIGN KEY(ProductDetailId) REFERENCES [tbl_ProductDetail](ProductDetailId)
)

CREATE TABLE [tbl_UserBookmark] (
	UserId			INT	NOT NULL,
	ProductDetailId	INT	NOT NULL

	CONSTRAINT PK_UserBookmark PRIMARY KEY(UserId, ProductDetailId),
	CONSTRAINT FK_UserBookMark_User FOREIGN KEY(UserId) REFERENCES [tbl_User](UserId),
	CONSTRAINT FK_UserBookmark_ProductDetail FOREIGN KEY(ProductDetailId) REFERENCES [tbl_ProductDetail](ProductDetailId)
)


-- INTIALIZE

INSERT INTO dbo.tbl_Product VALUES
('IPhone 13')
,('IPhone 14')
,('Samsung Galaxy S21')
,('Samsung Galaxy S22')

INSERT INTO dbo.tbl_ProductDetail VALUES
('Pro', 2022, '128GB', 1)
,('Pro Max', 2022, '128GB', 1)
,('Plus', 2022, '128GB', 2)
,('Standard', 2022, '64GB', 3)

INSERT INTO dbo.tbl_Source VALUES
('Amazon', 'www.amazon.ca')
,('Best Buy', 'www.bestbuy.ca')

INSERT INTO dbo.tbl_PriceDetail VALUES
(GETDATE(), 1700, 1, 1)
,(GETDATE(), 1900, 2, 1)
,(DATEADD(DAY, -1, GETDATE()), 2000, 1, 1)
,(DATEADD(DAY, -1, GETDATE()), 2000, 2, 1)
,(DATEADD(DAY, -29, GETDATE()), 1700, 1, 1)
,(DATEADD(DAY, -29, GETDATE()), 2100, 2, 1)
,(DATEADD(DAY, -60, GETDATE()), 2000, 1, 1)
,(DATEADD(DAY, -60, GETDATE()), 2000, 2, 1)
,(DATEADD(DAY, -90, GETDATE()), 1800, 1, 1)
,(DATEADD(DAY, -90, GETDATE()), 2000, 2, 1)
,(GETDATE(), 500, 1, 2)
,(GETDATE(), 600, 2, 2)
,(DATEADD(DAY, -1, GETDATE()), 400, 1, 2)
,(DATEADD(DAY, -1, GETDATE()), 400, 2, 2)