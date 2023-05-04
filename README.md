# Festival-App

Festival Web App with Ticket System

![payment-chart](https://user-images.githubusercontent.com/120065120/236341680-2cfc5a16-463d-40ba-bccf-bba535881dc3.png)

## Content
- [Features](https://github.com/erkamesen/Festival-App/blob/master/README.md#features)
- [Technologies](https://github.com/erkamesen/Festival-App/blob/master/README.md#technologies)
- [Installation & Usage](https://github.com/erkamesen/Festival-App/blob/master/README.md#installation--usage)


## Features
- *Users can track activities.*
- *Users can get in touch so they don't have any questions.*
- *Payment system integration is provided.*
- *Users can choose from 6 different ticket categories and buy tickets.*
- *A unique ticket code is created in the database when the ticket is purchased.*
- *In the requests sent to the /ticket path with the ticketNo argument, the value is checked and if it exists in the database, <br>
the QRCode of the ticket is created by image processing and displayed to the user.*
- *After the generated qrcode is processed on the ticket, it is deleted so that it does not take up space.*
- *The ticket created to the user is sent by e-mail.*
- *Successful and unsuccessful payment transactions are logged.*


## Technologies 
<div align=center>
<img src=https://user-images.githubusercontent.com/25181517/192107854-765620d7-f909-4953-a6da-36e1ef69eea6.png wirdth=60 height=60>
<img src=https://user-images.githubusercontent.com/25181517/192158954-f88b5814-d510-4564-b285-dff7d6400dad.png wirdth=60 height=60>
<img src=https://user-images.githubusercontent.com/25181517/183898674-75a4a1b1-f960-4ea9-abcb-637170a00a75.png wirdth=60 height=60>
<img src=https://user-images.githubusercontent.com/25181517/117447155-6a868a00-af3d-11eb-9cfe-245df15c9f3f.png wirdth=60 height=60>
<img src=https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png wirdth=60 height=60>
<img src=https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png wirdth=60 height=60>
</div>


## Installation & Usage

- *Clone the repository:*
```
git clone https://github.com/erkamesen/Festival-App.git
```
- *Navigate to the directory:*
```
cd Festival-App
```
- *To get started with the Festival-App, you'll need to have the following dependencies installed on your machine:*
- *install the requirements:*
```
pip install -r requirements.txt
```
- *Set Telegram token*
- *Set SMTP token*
- *Set IYZICO token*
- *Run the application:*
```
flask run
```
*Festival-App should now be running on your local machine at http://localhost:5000*

## Snaps

<h4 > Index </h4> 
<img src=https://user-images.githubusercontent.com/120065120/236341582-4977a87e-a5f6-46a7-b017-975d63fd5e0c.png>
<div>

<h4 > Pricing </h4> 
<img src=https://user-images.githubusercontent.com/120065120/236341518-be2ebff4-7ef7-4848-8f83-82390523b73e.png>
<div>

<h4 > Payment </h4> 
<img src=https://user-images.githubusercontent.com/120065120/236341439-492d5fa8-d08a-4b38-99a6-2f614f305958.png>
<div>

<div align=center>
<h4 > Ticket </h4> 
<img src=https://user-images.githubusercontent.com/120065120/236341299-e5c5da1f-cd87-454e-b5ae-9d7167986c5b.png>
<div>

<h4 > Telegram </h4> 
<img src=https://user-images.githubusercontent.com/120065120/236341383-b3c1e636-b47e-49c8-83ab-b8d04def20be.png>
<div>

