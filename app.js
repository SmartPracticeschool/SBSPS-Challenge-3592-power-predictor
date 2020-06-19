require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const ejs = require("ejs") 
const mongoose = require('mongoose');

const session = require('express-session');
const passport = require('passport');
const passportLocalMongoose = require('passport-local-mongoose');

const app = express();


app.use(express.static("public"));
app.set("view engine", 'ejs');
app.use(bodyParser.urlencoded({
    extended: true
}));

//below all the uses function
app.use(session({
    secret: "our little secret.",
    resave: false,
    saveUninitialized: false
}));

//initialize passport
app.use(passport.initialize());
app.use(passport.session());


// connect to Database
//mongoose.connect("mongodb://localhost:27017/userDB", {useNewUrlParser: true, useUnifiedTopology: true});
mongoose.connect(`mongodb+srv://${process.env.USER}:${process.env.PASS}@cluster0-y70r4.mongodb.net/todolistDB`, { useUnifiedTopology: true, useNewUrlParser: true })
    .then(() => console.log( 'Database Connected' ))
    .catch(err => console.log( err ));
mongoose.set('useCreateIndex', true);

//user schema
const userSchema = new mongoose.Schema({
   email: String,
   First_Name: String,
   Last_Name: String,
   password: String
});

userSchema.plugin(passportLocalMongoose);

const User = new mongoose.model("User", userSchema);

//create strategy
passport.use(User.createStrategy());

passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

// route to homepage
app.get("/", function(req, res){
    res.render("home");
});

//route to login page
app.get("/login", function(req, res){
   res.render("login", {SignError: ``});
});
app.get("/login/:error", function(req, res){
    res.render("login", {SignError: req.params.error});
});

//route to signUp page
app.get("/signUp", function(req, res){
   res.render("signUp", {SignError:``});
});
app.get("/signUp/:error", function(req, res){
    res.render("signUp", {SignError:req.params.error});
 });

//route to page of user who is logged in 
app.get("/userPage", (req, res) => {
   if(req.isAuthenticated()) res.render("userPage");
   else res.redirect("/login");
});

app.get("/logout", (req, res) => {
   req.logout();
   res.redirect("/");
}); 

//post register informations
app.post("/signUp", (req, res) => {
    // check for password
    if(req.body.password != req.body.Cpassword){
        res.redirect('signUp/Not Matching Password');
    }
    
    //1. check for uniqueness of email id
    User.findOne({username: req.body.username}, (err, result) => {
        if(err) res.send;
        else if(result) res.redirect("signUp/Email Id Already Exist")  //res.send("Email Id Already Exist");
        else {
            //2. First we need to verify the email address
            

            //3. Then write in database
            //console.log(req.body);
            
            User.register({ username: req.body.username, First_Name: req.body.Fname, Last_Name: req.body.Lname}, req.body.password, (err, user) => {
                //console.log(user);
                
                if (err) console.log(err);
                else if(user)res.redirect("/login");
                else res.redirect("/signUp");
            });
        }
    });
});

//authenticate user login data
app.post("/login", passport.authenticate('local', { successRedirect: '/userPage',
       failureRedirect: '/login/Username or Password is invalid' })
       
       
       //if(flag) res.render("login", {SignError: `Username or Password is invalid`});    
   
   
);

let port = process.env.PORT;

if(port == "" || port == null) port = 3000;

app.listen(port, (req, res) => {
   console.log(`server is listening at port ${port}`);
   
})