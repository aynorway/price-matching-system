IF NOT EXISTS ( SELECT * FROM sys.databases WHERE name = 'PriceMatchingSystem' )
BEGIN
    CREATE DATABASE [PriceMatchingSystem]
END
GO

USE [PriceMatchingSystem]
GO

DROP TABLE IF EXISTS [UserBookmark];
DROP TABLE IF EXISTS [Login];
DROP TABLE IF EXISTS [User];
DROP TABLE IF EXISTS [Admin];
DROP TABLE IF EXISTS [PriceDetail];
DROP TABLE IF EXISTS [Source];
DROP TABLE IF EXISTS [ProductDetail];
DROP TABLE IF EXISTS [Product];


CREATE TABLE [User] (
    UserId		INT				NOT NULL IDENTITY,
    UserName	NVARCHAR(50)	NOT NULL,
	FirstName	NVARCHAR(50)	NOT NULL,
	LastName	NVARCHAR(50)	NOT NULL,
	Address1	NVARCHAR(50),
	Address2	NVARCHAR(50),
	City		NVARCHAR(50),
	Province	NVARCHAR(50),
	Country		NVARCHAR(50),
	PostalCode	NVARCHAR(20),
	Phone		NVARCHAR(20),
	PhotoURL	NVARCHAR(50)

	CONSTRAINT PK_User PRIMARY KEY(UserId)
)

CREATE TABLE [Login] (
	LoginId		INT				NOT NULL IDENTITY,
	Email		NVARCHAR(50)	NOT NULL,
	Password	NVARCHAR(100)	NOT NULL,
	UserId		INT				NOT NULL

	CONSTRAINT PK_Login PRIMARY KEY(LoginId),
	CONSTRAINT FK_Login_User FOREIGN KEY(UserId) REFERENCES [User](UserId)
)

CREATE TABLE [Admin] (
	AdminId		INT				NOT NULL IDENTITY,
	AdminName	NVARCHAR(50)	NOT NULL,
	Password	NVARCHAR(100)	NOT NULL

	CONSTRAINT PK_Admin PRIMARY KEY(AdminId),
)

CREATE TABLE [Product] (
	ProductId	INT				NOT NULL IDENTITY,
	ProductName	NVARCHAR(50)	NOT NULL,

	CONSTRAINT PK_Product PRIMARY KEY(ProductId),
)

CREATE TABLE [ProductDetail] (
	ProductDetailId		INT				NOT NULL IDENTITY,
	Model				NVARCHAR(50)	NOT NULL,
	Year				INT				NOT NULL,
	Storage				NVARCHAR(50)	NOT NULL,
	ProductId			INT				NOT NULL 

	CONSTRAINT PK_ProductDetail PRIMARY KEY(ProductDetailId),
	CONSTRAINT FK_ProductDetail_Product FOREIGN KEY(ProductId) REFERENCES [Product](ProductId)
)

CREATE TABLE [Source] (
	SourceId	INT				NOT NULL IDENTITY,
	SourceName	NVARCHAR(50)	NOT NULL,
	SourceURL	NVARCHAR(50)	NOT NULL,

	CONSTRAINT PK_Source PRIMARY KEY(SourceId)
)

CREATE TABLE [PriceDetail] (
	PriceDetailId		INT		NOT NULL IDENTITY,
	PriceDetailDate		DATE	NOT NULL,
	Price				MONEY	NOT NULL,
	SourceId			INT		NOT NULL,
	ProductDetailId		INT		NOT NULL

	CONSTRAINT PK_PriceDetail PRIMARY KEY(PriceDetailId),
	CONSTRAINT FK_PriceDetail_Source FOREIGN KEY(SourceId) REFERENCES [Source](SourceId),
	CONSTRAINT FK_PriceDetail_ProductDetail FOREIGN KEY(ProductDetailId) REFERENCES [ProductDetail](ProductDetailId)
)

CREATE TABLE [UserBookmark] (
	UserId			INT	NOT NULL,
	ProductDetailId	INT	NOT NULL

	CONSTRAINT PK_UserBookmark PRIMARY KEY(UserId, ProductDetailId),
	CONSTRAINT FK_UserBookMark_User FOREIGN KEY(UserId) REFERENCES [User](UserId),
	CONSTRAINT FK_UserBookmark_ProductDetail FOREIGN KEY(ProductDetailId) REFERENCES [ProductDetail](ProductDetailId)
)