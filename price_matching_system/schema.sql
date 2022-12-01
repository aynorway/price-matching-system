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
	Address1	NVARCHAR(250),
	Address2	NVARCHAR(250),
	City		NVARCHAR(250),
	Province	NVARCHAR(250),
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
	ProductId			INT				NOT NULL,
	ProductPhotoURL		NVARCHAR(250)	NULL

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
('Apple IPhone 13')
,('Apple IPhone 14')
,('Samsung Galaxy S21')
,('Samsung Galaxy S22')
,('Google Pixel 6')
,('Google Pixel 7')
,('MacBook Air')
,('MacBook Pro')
,('ThinkPad P1')
,('Dell Alienware x17')
,('Huawei MateBook')


INSERT INTO dbo.tbl_ProductDetail VALUES
('Pro', 2022, '128GB', 1, 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-pro-01.jpg')
,('Pro Max', 2022, '128GB', 1, 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-pro-max-01.jpg')
,('', 2022, '128GB', 1, 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-01.jpg')
,('', 2022, '128GB', 2, 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-3.jpg')
,('', 2022, '64GB', 3, 'https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s21-5g-0.jpg')
,('Ultra 5G', 2022, '64GB', 4, 'https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s22-ultra-5g-2.jpg')
,('Pro', 2021, '128GB', 5, 'https://fdn2.gsmarena.com/vv/pics/google/google-pixel-6-pro-1.jpg')
,('', 2022, '128GB', 6, 'https://fdn2.gsmarena.com/vv/pics/google/google-pixel7-2.jpg')
,('M2"', 2022, '512GB', 6, 'https://nanoreview.net/common/images/laptop/apple-macbook-air-m2-2022-mini.jpeg')
,('16"', 2022, '512GB', 6, 'https://nanoreview.net/common/images/laptop/apple-macbook-pro-13-2019-mini.jpeg')
,('Gen 5 Intel (16”)', 2022, '512GB', 6, 'https://nanoreview.net/common/images/laptop/lenovo-thinkpad-p1-gen-5-mini.jpeg')
,('R2', 2022, '128GB', 6, 'https://nanoreview.net/common/images/laptop/dell-alienware-x17-r2-mini.jpeg')
,('14"', 2022, '512GB', 6, 'https://nanoreview.net/common/images/laptop/huawei-matebook-14-mini.jpeg')

INSERT INTO dbo.tbl_Source VALUES
('Amazon', 'www.amazon.ca')
,('Best Buy', 'www.bestbuy.ca')

INSERT INTO dbo.tbl_PriceDetail VALUES
(GETDATE(), 700, 1, 1)
,(GETDATE(), 700, 2, 1)
,(DATEADD(DAY, -1, GETDATE()), 800, 1, 1)
,(DATEADD(DAY, -1, GETDATE()), 850, 2, 1)
,(DATEADD(DAY, -29, GETDATE()), 700, 1, 1)
,(DATEADD(DAY, -29, GETDATE()), 750, 2, 1)
,(DATEADD(DAY, -60, GETDATE()), 700, 1, 1)
,(DATEADD(DAY, -60, GETDATE()), 800, 2, 1)
,(DATEADD(DAY, -90, GETDATE()), 850, 1, 1)
,(DATEADD(DAY, -90, GETDATE()), 800, 2, 1)

,(GETDATE(), 500, 1, 2)
,(GETDATE(), 600, 2, 2)
,(DATEADD(DAY, -1, GETDATE()), 400, 1, 2)
,(DATEADD(DAY, -1, GETDATE()), 300, 2, 2)

,(DATEADD(DAY, -1, GETDATE()), 800, 1, 3)
,(DATEADD(DAY, -1, GETDATE()), 900, 2, 3)
,(DATEADD(DAY, -29, GETDATE()), 800, 1, 3)
,(DATEADD(DAY, -29, GETDATE()), 950, 2, 3)
,(DATEADD(DAY, -60, GETDATE()), 850, 1, 3)
,(DATEADD(DAY, -60, GETDATE()), 700, 2, 3)
,(DATEADD(DAY, -90, GETDATE()), 750, 1, 3)
,(DATEADD(DAY, -90, GETDATE()), 800, 2, 3)

,(DATEADD(DAY, -1, GETDATE()), 1400, 1, 4)
,(DATEADD(DAY, -1, GETDATE()), 1200, 2, 4)
,(DATEADD(DAY, -29, GETDATE()), 1700, 1, 4)
,(DATEADD(DAY, -29, GETDATE()), 2100, 2, 4)
,(DATEADD(DAY, -60, GETDATE()), 900, 1, 4)
,(DATEADD(DAY, -60, GETDATE()), 2000, 2, 4)
,(DATEADD(DAY, -90, GETDATE()), 1800, 1, 4)
,(DATEADD(DAY, -90, GETDATE()), 2000, 2, 4)

,(DATEADD(DAY, -1, GETDATE()), 200, 1, 5)
,(DATEADD(DAY, -1, GETDATE()), 250, 2, 5)
,(DATEADD(DAY, -29, GETDATE()), 220, 1, 5)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 5)
,(DATEADD(DAY, -60, GETDATE()), 150, 1, 5)
,(DATEADD(DAY, -60, GETDATE()), 200, 2, 5)
,(DATEADD(DAY, -90, GETDATE()), 250, 1, 5)
,(DATEADD(DAY, -90, GETDATE()), 200, 2, 5)

,(DATEADD(DAY, -1, GETDATE()), 1000, 1, 6)
,(DATEADD(DAY, -1, GETDATE()), 900, 2, 6)
,(DATEADD(DAY, -29, GETDATE()), 950, 1, 6)
,(DATEADD(DAY, -29, GETDATE()), 900, 2, 6)
,(DATEADD(DAY, -60, GETDATE()), 880, 1, 6)
,(DATEADD(DAY, -60, GETDATE()), 800, 2, 6)
,(DATEADD(DAY, -90, GETDATE()), 1000, 1, 6)
,(DATEADD(DAY, -90, GETDATE()), 1000, 2, 6)

,(DATEADD(DAY, -1, GETDATE()), 300, 1, 7)
,(DATEADD(DAY, -1, GETDATE()), 255, 2, 7)
,(DATEADD(DAY, -29, GETDATE()), 295, 1, 7)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 7)
,(DATEADD(DAY, -60, GETDATE()), 200, 1, 7)
,(DATEADD(DAY, -60, GETDATE()), 250, 2, 7)
,(DATEADD(DAY, -90, GETDATE()), 250, 1, 7)
,(DATEADD(DAY, -90, GETDATE()), 300, 2, 7)

,(DATEADD(DAY, -1, GETDATE()), 400, 1, 8)
,(DATEADD(DAY, -1, GETDATE()), 450, 2, 8)
,(DATEADD(DAY, -29, GETDATE()), 400, 1, 8)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 8)
,(DATEADD(DAY, -60, GETDATE()), 400, 1, 8)
,(DATEADD(DAY, -60, GETDATE()), 300, 2, 8)
,(DATEADD(DAY, -90, GETDATE()), 450, 1, 8)
,(DATEADD(DAY, -90, GETDATE()), 400, 2, 8)

,(DATEADD(DAY, -1, GETDATE()), 400, 1, 9)
,(DATEADD(DAY, -1, GETDATE()), 450, 2, 9)
,(DATEADD(DAY, -29, GETDATE()), 400, 1, 9)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 9)
,(DATEADD(DAY, -60, GETDATE()), 400, 1, 9)
,(DATEADD(DAY, -60, GETDATE()), 300, 2, 9)
,(DATEADD(DAY, -90, GETDATE()), 450, 1, 9)
,(DATEADD(DAY, -90, GETDATE()), 400, 2, 9)

,(DATEADD(DAY, -1, GETDATE()), 400, 1, 10)
,(DATEADD(DAY, -1, GETDATE()), 450, 2, 10)
,(DATEADD(DAY, -29, GETDATE()), 400, 1, 10)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 10)
,(DATEADD(DAY, -60, GETDATE()), 400, 1, 10)
,(DATEADD(DAY, -60, GETDATE()), 300, 2, 10)
,(DATEADD(DAY, -90, GETDATE()), 450, 1, 10)
,(DATEADD(DAY, -90, GETDATE()), 400, 2, 10)

,(DATEADD(DAY, -1, GETDATE()), 400, 1, 11)
,(DATEADD(DAY, -1, GETDATE()), 450, 2, 11)
,(DATEADD(DAY, -29, GETDATE()), 400, 1, 11)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 11)
,(DATEADD(DAY, -60, GETDATE()), 400, 1, 11)
,(DATEADD(DAY, -60, GETDATE()), 300, 2, 11)
,(DATEADD(DAY, -90, GETDATE()), 450, 1, 11)
,(DATEADD(DAY, -90, GETDATE()), 400, 2, 11)

,(DATEADD(DAY, -1, GETDATE()), 400, 1, 12)
,(DATEADD(DAY, -1, GETDATE()), 450, 2, 12)
,(DATEADD(DAY, -29, GETDATE()), 400, 1, 12)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 12)
,(DATEADD(DAY, -60, GETDATE()), 400, 1, 12)
,(DATEADD(DAY, -60, GETDATE()), 300, 2, 12)
,(DATEADD(DAY, -90, GETDATE()), 450, 1, 12)
,(DATEADD(DAY, -90, GETDATE()), 400, 2, 12)

,(DATEADD(DAY, -1, GETDATE()), 400, 1, 13)
,(DATEADD(DAY, -1, GETDATE()), 450, 2, 13)
,(DATEADD(DAY, -29, GETDATE()), 400, 1, 13)
,(DATEADD(DAY, -29, GETDATE()), 300, 2, 13)
,(DATEADD(DAY, -60, GETDATE()), 400, 1, 13)
,(DATEADD(DAY, -60, GETDATE()), 300, 2, 13)
,(DATEADD(DAY, -90, GETDATE()), 450, 1, 13)
,(DATEADD(DAY, -90, GETDATE()), 400, 2, 13)
