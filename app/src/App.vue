<template>
  <div id="app">
    <dashboard v-model="activeui" />

    <flash-messages></flash-messages>
    <page-add
        v-if="activeui === 'PROTOCOL_ADD'"
        v-model="protocol"
        :organizations="organizations"
        :facilities="facilities"
        :persons="persons"
        :categories="categories"
        :inspection-standards="inspectionStandards">
    </page-add>
  </div>
</template>

<script>
import Dashboard from './components/Dashboard'
import FlashMessages from './components/FlashMessages'

import PageAdd from './components/PageAdd'
import PageLoad from './components/PageLoad'

import { EventBus } from "./EventBus.js";

const $ = require('jquery');

export default {
    name: 'app',
    components: {
        Dashboard,
        FlashMessages,
        PageAdd,
        PageLoad,
    },
    data: function() {
        return {
            flashMessages: [],
            activeui: 'MAIN_MENU',
            protocol: {
                id: null,
                header: {},
                entries: []
            },

            organizations: [
                { repr: 'HELLO', data: { _id: 'org_1' } },
                { repr: 'HELL2', data: { _id: 'org_2' } },
                { repr: 'LLOO3', data: { _id: 'org_3' } },
                { repr: 'FRANK', data: { _id: 'org_4' } },
                { repr: 'FFRANK', data: { _id: 'org_5' } },
            ],
            facilities: [
                { repr: 'FASSS', data: { _id: 'fac_1' } },
                { repr: 'LALSKS', data: { _id: 'fac_2' } },
            ],
            persons: [
                { repr: 'PPERSON', data: { _id: 'per_1' } },
                { repr: 'AMAAMA', data: { _id: 'per_2' } },
            ],
            inspectionStandards: [
                { repr: 'INSPA', data: { _id: 'insp_1' } },
                { repr: 'KASLDJASL', data: { _id: 'insp_2' } },
            ],
            categories: [
                { repr: 'CATEAAG', data: { _id: 'cat_1' } },
                { repr: 'M;ASNDMA;', data: { _id: 'cat_2' } },
            ]
        }
    },
    created: function() {
        EventBus.$on('newFacilityAdded', (e) => this.facilities.push(e));
        EventBus.$on('newOrganizationAdded', (e) => this.organizations.push(e));
        EventBus.$on('newPersonAdded', (e) => this.persons.push(e));
        EventBus.$on('newCategoryAdded', (e) => this.categories.push(e));
        EventBus.$on('newInspectionStandardAdded', (e) => this.inspectionStandards.push(e));

        /*
        this.fetchOrganizations();
        this.fetchFacilities();
        this.fetchPersons();
        this.fetchCategories();
        this.fetchInspectionStandards();
        */
    },
    methods: {
        log: function(e) {
            console.log(e);
        },
        submitNewForm: function() {

        },
        fetchCategories: function() {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:5000/categories/',
                data: {},
                success: function(result, status) {
                    console.log('FETCHED CATEGORIES');
                    console.log(JSON.stringify(result));

                    this.categories = result.map((i) => { 
                        return {
                            repr: i.name,
                            data: i
                        };
                    });
                }
            });
        },
        fetchInspectionStandards: function() {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:5000/inspectionStandards/',
                data: {},
                success: function(result, status) {
                    console.log('FETCHED INSPECTION_STANDARDS');
                    console.log(JSON.stringify(result));

                    this.inspectionStandards = result.map((i) => { 
                        return {
                            repr: i.name,
                            data: i
                        };
                    });
                }
            });
        },
        fetchOrganizations: function() {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:5000/organizations/',
                data: {},
                success: function(result, status) {
                    console.log('FETCHED ORGANIZATIONS');
                    console.log(JSON.stringify(result));

                    this.organizations = result.map((i) => { 
                        return {
                            repr: i.name,
                            data: i
                        };
                    });
                }
            });
        },
        fetchFacilities: function() {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:5000/facilities/',
                data: {},
                success: function(result, status) {
                    console.log('FETCHED FACILITIES');
                    console.log(JSON.stringify(result));

                    this.facilities = result.map((i) => { 
                        return {
                            repr: i.name,
                            data: i
                        };
                    });
                }
            });
        },
        fetchPersons: function() {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:5000/persons/',
                data: {},
                success: function(result, status) {
                    console.log('FETCHED PERSONS');
                    console.log(JSON.stringify(result));

                    this.persons = result.map((i) => { 
                        return {
                            repr: i.name + ', ' + i.firstName,
                            data: i
                        };
                    });
                }
            });
        },
        get: function() {
            let data = {
                collection: 'testcollection',
                q: 'hello',
                on: 'testkey'
            };
            $.ajax({
                type: 'GET',
                url: 'http://localhost:5000/_suggestions/',
                data: data,
                success: function(result, status) {
                    console.log(result);
                }
            });
        },
        put: function() {
            let data = {
                collection: 'testcollection',
                data: {
                    testkey: 'helloworld',
                    otherkey: 'byeworld'
                }
            };
            $.ajax({
                type: 'POST',
                url : 'http://localhost:5000/_data/',
                data : JSON.stringify(data, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(result, status) {
                    console.log(result);
                }
            });
        }
    }
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
</style>
