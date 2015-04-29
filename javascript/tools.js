/**
Main.js

A library of common javascript functions.  Used to keep the templates a bit cleaner.
Common functions should not have any tag names hard coded into them.  If they must
Access an html element directly, pass in the tag object as a parameter.
**/

//Python's bools are uppercase, this allows me to use them without any transformations
True = true
False = false

ERROR_BLANK = "ERROR_BLANK";
ERROR_BAD_CHARS = "ERROR_BAD_CHARS";
ERROR_TOO_SHORT = "ERROR_TOO_SHORT";

//scrabble scores dictionary
scrabbleKey = {
                "a":1,
                "b":3,
                "c":3,
                "d":2,
                "e":1,
                "f":4,
                "g":2,
                "h":4,
                "i":1,
                "j":8,
                "k":5,
                "l":1,
                "m":3,
                "n":1,
                "o":1,
                "p":3,
                "q":10,
                "r":1,
                "s":1,
                "t":1,
                "u":1,
                "v":4,
                "w":4,
                "x":8,
                "y":4,
                "z":10,
           };

//WWF scores dictionary
wwfKey = {
                "a":1,
                "b":4,
                "c":4,
                "d":2,
                "e":1,
                "f":4,
                "g":3,
                "h":3,
                "i":1,
                "j":10,
                "k":5,
                "l":2,
                "m":4,
                "n":2,
                "o":1,
                "p":4,
                "q":10,
                "r":1,
                "s":1,
                "t":1,
                "u":2,
                "v":5,
                "w":4,
                "x":8,
                "y":3,
                "z":10,
           };

inputRegex = /^[a-z]*$/; //Only a-z Chars!
failColor = "#800080";//dark purple
successColor = "#376A82";//dull blue/green
defaultColor = "#000000";//Black
defaultInterval = 1000;//about a 1 second transition
screenSize = "Default";//the current screen size

//given a word and a scoreDictionary, get that word's score
function getScore(word, scoreDictionary){
    var score = 0;
    var word = word.toLowerCase();
    for( var i = 0; i < word.length; i++){
        if(word[i] in scoreDictionary){
            score += scoreDictionary[word[i]];
        }
        else{
            return 0;
        }
    }
    return score;
}

//returns true if the browser is Internet Explorer
function usingIE() {
    /** //came from http://stackoverflow.com/questions/19999388/jquery-check-if-user-is-using-ie
        var ua = window.navigator.userAgent;
        var msie = ua.indexOf("MSIE ");

        if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)){
            //alert(parseInt(ua.substring(msie + 5, ua.indexOf(".", msie)))); //gets ie version number
            out = true;
        }else{
            out = false;
        }
        return out; */
    //single line version, original came from internet, too lazy to dissect it - it works
    return (window.navigator.userAgent.indexOf("MSIE ") > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./));
}



//Sets the background color of the page
function setBackground(color,interval){
  jQuery("body").animate({
      backgroundColor: color
  }, interval );
}

//clears the page if out of date
function handleVersion(upToDate){
    if(!upToDate){
       localStorage.clear();
    }
}

/**
 * Validates a word and returns a boolean stating if it passed the
 * validation and a string with either the cleaned input or the error text
 **/
function validateWord(input){
    var input = input.val().trim().toLowerCase();//cleans the input by making it lowercase and removing excess whitespace
    var retVal;
    if(input.length == 0){//if blank or only whitespace
        retVal = [false, ERROR_BLANK];
    } else if( input.length == 1 ) {
        retVal = [false, ERROR_TOO_SHORT];
    } else if(input.match(inputRegex) == null){//if it has non a-z chars
        retVal = [false,ERROR_BAD_CHARS];
    } else {//if good input
        retVal = [true,input];
    }
    return retVal;//return false,"" if invalid and True,cleanInput if valid
}

//handles caching of a word, the word's permalink, and the definition
function cacheHandler(word, wordId, definition){
    prefix = wordId ? "http://www.isthataword.net/direct/" : ""; //adds the proper address if the word is found and a blank if it's empty
    cacheData(word.concat("_permalink"),prefix.concat(wordId)) //caches the word and its permalink. (ex: word is test, the values are ["test_permalink":"http://www.isthataword.net/direct/wordId"]
    cacheData(word, definition); //caches the word and html definition
}

//for right now, just empty local storage if there's a problem
function cacheData(key, value){
    try{
        localStorage.setItem(key,value);
    } catch(err){
        localStorage.clear()
    } finally {
        localStorage.setItem(key,value);
    }
    return;
}

//checks if data has been cached
function dataIsCached(input){
    return localStorage.getItem(input) != null;
}

/**
  * Sets the definitions for the definition div
  *
  * defintionDiv - HTML element for a div that holds all the definition Data
  * data - definition data to be added into the definition div
  * showingDefinitions - states whether to show or hide the definition div
 **/
function setDefinitions(definitionDiv, data, showingDefinitions){
    definitionDiv.html(data);
    if(!canPlayAudio()){
        $(".audio").hide();
    }
    if(showingDefinitions){
        definitionDiv.show();
    } else {
        definitionDiv.hide();
    }
}

//checks if browser can play HTML5 audio
function canPlayAudio(){
    var a = document.createElement('audio');
    return !!(a.canPlayType && a.canPlayType('audio/wav; codecs="1"').replace(/no/, ''));
}

//Gets the definition for a given word
function getAndSetDefinitions(input, wordId, outputDiv){
    $.ajax({
        type: 'GET',
        url: '/define',
        data: {input_str: input },
        success: function(data){
            if(data == ""){
                data = "<div class='inputError'>While ".concat(input).concat(" is a word, we don't have a defintion for it at this time!</div>");
            }
            cacheHandler(input, wordId, data)
            setDefinitions(outputDiv, data, true);
        },
        dataType: 'html'
    });
}

//update Scrabble and WWF scores
function updateScores(word, scrabbleText, wwfText){
    scrabbleText.text(getScore(word, scrabbleKey));
    wwfText.text(getScore(word, wwfKey));
}
