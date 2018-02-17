<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>

body {
  font-family: Arial, Helvetica, sans-serif;
}
.sep-line-small hr {
  height: 2px;
  background-color: #303F9F;
  margin-left: 25px;
  margin-right: 25px;
}

div#forms {
    position: absolute;
    top: 70px;
    width: 100%;
}
form {
    margin-left: auto;
    margin-right: auto;
    margin-top: 10px;
    margin-bottom: 10px;
    position: relative;
    width: 850px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1em;
    font-style: italic;
    line-height: 24px;
    font-weight: bold;
    color: #303F9F;
    text-decoration: none;
    border-radius: 2px;
    padding: 10px;
    border: 1px solid #303F9F;
    border: inset 1px solid #333;
    -webkit-box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
    -moz-box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
    box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
}

label {
    display: block;
    margin: 0;
}

label > span {
    float: left;
    padding-right: 20px;
    text-align: right;
    width: 20%;
    margin-top: 9px;
}

textarea {
    width: 411px;
    height: 200px;
    resize: vertical;
    font-size: 1em;
    padding: 3px;
    margin-top: 7px;
    margin-bottom: 7px;
    font-family: inherit;
}

input[type=text], input[type=number], input[type=file], input[type=date], input[type=email], select {
    width: 414px;
    height: 27px;
    font-size:1em; 
    text-indent:10px; 
    outline: 0 none;
    color:#333; 
    background: #fff; 
    border:solid 1px #d9d9d9; 
    border-top:solid 1px #c0c0c0; 
    margin-top: 7px;
    margin-bottom: 7px;
}

input[type=file] {
    padding-top: 5px;
    padding-bottom: 5px;
}

input[type=radio] {
    border: 1px solid #999;
    -webkit-box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
    -moz-box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
    box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
}

input[type=button] {
    position: relative;
    background: #E8EAF6;
    color: #303F9F;
    font-family: Tahoma, Geneva, sans-serif;
    height: 30px;
    border-radius: 7px;
    border: 1px solid #303F9F;
    cursor: pointer;
}

input[type=button]:hover {
    color: #E8EAF6;
    background: #303F9F;
}

input.btn-delete {
    border: none;
    background: rgb(243, 67, 67);
    color: rgb(255, 255, 255);
    font-weight: 700;
}
input.btn-delete:hover {
    background: rgb(192, 1, 1);
    color: rgb(255, 255, 255);
}

input[type=button]:disabled {
    cursor: not-allowed;
}

img {
    width: 45px;
    height: 45px;
    float: right;
}

.bubble{
    background-color: #FFF;
    border-radius: 5px;
    box-shadow: 0px 0px 6px #303F9F;
    position: absolute;
    min-width: 250px;
    min-height: 100px;
    z-index: 1;
    margin-left: 440px;
    margin-top: -30px;

}
.preview p {
    font-size:1em; 
    font-style: normal;
    font-weight: normal;
    font-family:arial, sans-serif; 
    text-indent:10px; 
    outline: 0 none;
    color:#333; 
    text-align: center;
    margin: 7px;
    padding: 5px;
}

</style>
