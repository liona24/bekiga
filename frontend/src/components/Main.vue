<template>
  <div>
    <dashboard v-model="activeui" />

    <flash-messages></flash-messages>
    <loader v-if="activeui === 'LOADING'"></loader>
    <page-add
        v-else-if="activeui === 'PROTOCOL_ADD'"
        v-model="protocol"
        :organizations="organizations"
        :facilities="facilities"
        :persons="persons"
        :categories="categories"
        :inspection-standards="inspectionStandards"
        @submit="submitProtocol">
    </page-add>
    <page-load
        v-else-if="activeui === 'PROTOCOL_LOAD'">
    </page-load>
  </div>
</template>

<script>
import Dashboard from './Dashboard'
import FlashMessages from './FlashMessages'
import Loader from './Loader'

import PageAdd from './PageAdd'
import PageLoad from './PageLoad'

import { EventBus } from "../EventBus.js";
import { postProtocol, fetch } from '../ajax.js';
import { urlRender } from '../urls.js';

const $ = require('jquery');

export default {
    name: 'Main',
    components: {
        Dashboard,
        FlashMessages,
        Loader,
        PageAdd,
        PageLoad,
    },
    data: function() {
        return {
            flashMessages: [],
            activeui: 'MAIN_MENU',
            protocol: {
                _id: null,
                header: {},
                entries: []
            },

            organizations: [],
            facilities: [],
            persons: [],
            inspectionStandards: [],
            categories: []
        }
    },
    created: function() {
        EventBus.$on('newFacilityAdded', (e) => {
            this.facilities.push(e)
            console.log(e);
        });
        EventBus.$on('newOrganizationAdded', (e) => this.organizations.push(e));
        EventBus.$on('newPersonAdded', (e) => this.persons.push(e));
        EventBus.$on('newCategoryAdded', (e) => this.categories.push(e));
        EventBus.$on('newInspectionStandardAdded', (e) => this.inspectionStandards.push(e));

        fetch('organizations/', 
            (i) => i.name,
            (res) => this.organizations = res
        );
        fetch('facilities/',
            (i) => i.name,
            (res) => this.facilities = res
        );
        fetch('persons/',
            (i) => i.name + ', ' + i.firstName,
            (res) => this.persons = res
        );
        fetch('categories/',
            (i) => i.name,
            (res) => this.categories = res
        );
        fetch('inspectionStandards/',
            (i) => i.name,
            (res) => this.inspectionStandards = res
        );
    },
    destroyed: function() {
        EventBus.$off('newFacilityAdded');
        EventBus.$off('newOrganizationAdded');
        EventBus.$off('newPersonAdded',);
        EventBus.$off('newCategoryAdded');
        EventBus.$off('newInspectionStandardAdded');
    },
    methods: {
        renderProtocol: function(_id) {
            window.open(urlRender + _id);
        },
        submitProtocol: function() {
            this.activeui = 'LOADING';
            postProtocol(this.protocol).then((_id) => {
                EventBus.$emit('flash', { msg: 'Neues Protokoll angelegt.', status: 'okay' });
                this.activeui = 'MAIN_MENU';
                this.protocol.header = {};
                this.protocol.entries = [];
                this.protocol._id = null;

                this.renderProtocol(_id);
            }, () => {
                this.activeui = 'MAIN_MENU';
                EventBus.$emit('flash', { msg: 'Protokoll konnte nicht angelegt werden!', status: 'error' });
            });
        },
    }
}
</script>
