<template>
  <div>
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
import Dashboard from './Dashboard'
import FlashMessages from './FlashMessages'

import PageAdd from './PageAdd'
import PageLoad from './PageLoad'

import { EventBus } from "../EventBus.js";

const $ = require('jquery');

export default {
    name: 'Main',
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
    destroyed: function() {
        EventBus.$off('newFacilityAdded');
        EventBus.$off('newOrganizationAdded');
        EventBus.$off('newPersonAdded',);
        EventBus.$off('newCategoryAdded');
        EventBus.$off('newInspectionStandardAdded');
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
