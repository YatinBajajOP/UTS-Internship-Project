# UTS-Internship-Project

Loan Risk Management Web Application for Banks dealing with agricultural loans

In this web application we are implementing different deep learning models/algorithms for different pages using TK solver, SQL and other applications.  We have made an application for farmers where he/she can apply for a loan from us after checking the eligibility of the farmer by calculating the risk on the basis of other factors which are helpful for the good crop harvesting. Along with-it farmer can upload the plot image and can see the segmentation of various areas of the image and their percentage of different segmented areas.

## Signup: [signup.py]
Customers and admin must sign up first to access the resources of the website.
Requirements for sign up are:
Name, phone number, unique user ID, aadhar number for customer users 

### Sign up as Customer

 ![image](https://user-images.githubusercontent.com/67017561/147593713-a42fc670-d5e3-410b-b264-bd94b0b53c11.png)

### Sign up as admin
![image](https://user-images.githubusercontent.com/67017561/147593758-13e7f75f-278f-4451-b5ad-c11054880f95.png)
     

If you need to sign up as an admin then tick the I am admin button and enter the unique admin id given to you by the company, other details are the same as customer details


## Login: [login.py]
After successful sign up a user can log in to access the different resources of the web application using a unique username and password


### Logged in as customer                                                 
   
![image](https://user-images.githubusercontent.com/67017561/147593807-9078452e-f50a-469b-ac57-cac2d36c067f.png)


### Logged in as admin 
 
![image](https://user-images.githubusercontent.com/67017561/147593822-87a5b45a-7da7-4365-b879-96088074deba.png)

## Visualization: [viz.py]
### Customer
![image](https://user-images.githubusercontent.com/67017561/147593848-1340b0a1-ce78-42ea-9e3b-422b12630169.png)

User is logged in as the customer can see the weather report of the place by entering the location. Weather reports consist of temperature, wind speed, description, and weather
Customer can also see previous uploads tick the check box show previous image uploaded 

![image](https://user-images.githubusercontent.com/67017561/147593864-c8750d90-25cf-4e6f-84ef-8c1fe10bd056.png)
	
![image](https://user-images.githubusercontent.com/67017561/147593872-1c2b99f2-f758-4672-b734-49919e235234.png)
 
Customers can also upload the image of the area to see the segmentation of the plot into the land, water, and other things in that image. To see the original image, tick the check box show image (as given in image above) and to see the output of the image then click the generate output button (as given in image below)

 
![image](https://user-images.githubusercontent.com/67017561/147593884-053469e6-6225-4763-9e53-04dc0454168d.png)

### Admin:

![image](https://user-images.githubusercontent.com/67017561/147593906-f6f27ff4-5583-48b3-8fc6-6de8d8412ede.png)

Users logged in as admin can see the user details in this page.
Two checkbox will be visible as 1). Show all user and 2). Details of the specific customer
Show all user: if admin will choose show all user then all the customer will be available into the tabular form as shown below
 
![image](https://user-images.githubusercontent.com/67017561/147593917-32984a7c-76e7-4315-ae99-d7e126ea424f.png)
 

Details of the specific customer: admin will enter the name of the customer whose information he/she wants to review and then click the check button.
eligibility details and file path details of that specific customer will appear into tabular form on the page
 
![image](https://user-images.githubusercontent.com/67017561/147593925-5bce6524-e5f0-44b0-85ca-2d57f5ed3319.png)


Check particular upload:
If admin will choose this option then text box will appear copy paste the path of the image and then click the display button 

![image](https://user-images.githubusercontent.com/67017561/147593935-24a4c1e9-e8ec-4da0-be1d-bd8476787d0a.png)


## Eligibility: [eligibility.py]

### Customer 
Go to the eligibility page and input the parameter according to you 
Customer will enter the details like NAME, AADHAR, and preferred crop (rice, maize, cotton)
  1.       Age:
  2.       Rainfall:
  3.       Debit:
  4.       Saving:
  5.       Weather:
  6.      Month of harvesting:   
After inputting all this information then click the submit button and Admin will return the customer with the eligibility score   

![image](https://user-images.githubusercontent.com/67017561/147594001-2e0751f4-74b4-42b0-bed5-d332bb9662b8.png)


Check the details into a form of table and bar graph 

![image](https://user-images.githubusercontent.com/67017561/147594020-b1714e16-8174-4a06-aa6f-2d032693d4f2.png)


### Admin

![image](https://user-images.githubusercontent.com/67017561/147594051-8556e6c5-5e53-4e21-8fd1-6a50d36d8338.png)
 	       
Show all details
![image](https://user-images.githubusercontent.com/67017561/147594061-a0ce4a0e-2cfc-4f35-91a9-1e6a73d258cd.png)

 
In show all details, details of every customer will be displayed in the form of table 


Details of specific customer

![image](https://user-images.githubusercontent.com/67017561/147594078-ae3d10c8-c03c-44f6-9949-771358e9d5a7.png)


Details of the specific customer can be fetched by the Aadhar number of the customer
To calculate the eligibility score admin can click the calculate score button  

### Loan: [loan.py]

If customer is eligible for loan, they can input the parameters:
This form consists of the parameters on which the loan will be sanctioned to the customer
1. Loan: this factor will allow the customer to decide the amount of loan he/she wants. It is in a form of a slider bar with maximum value and minimum value as 2500000 and 50000 respectively
2. Fees: this parameter consists of the fees which the bank will charge from the customer for a loan this will vary from 0 to 100000
3. Tenure: period till which loan is required by the customer
4. Rate: on what rate customer require a loan
5. Emi: EMI will be calculated by the TK solver and tell the customer the total EMI using parameter loan, rate, and tenure
6. Interest Amount: it is a function that is calculated by the TK solver on the above parameter on loan and rate
7. Repayment: all the amount that farmers need to pay after adding interest and loan amount.


Customer: when the user is logged in as customer and the eligibility criteria met then farmer can apply for loan by inputting all the parameters which are described above. then click on the apply button to see the total repayment of the loan 

![image](https://user-images.githubusercontent.com/67017561/147594107-adcfade2-6544-483d-9f5a-7aa4233e8758.png)
![image](https://user-images.githubusercontent.com/67017561/147594116-406f8cb5-df7c-4b5b-bfae-2d61e1e4cc5b.png)


### Admin:
Admin can see the details of the farmer who has applied for the loan.
![image](https://user-images.githubusercontent.com/67017561/147594129-018002fa-0970-4232-bb38-ddadea0c5387.png)


