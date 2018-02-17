<template>
  <div>
    <div id="dashboard">
        <div class="dashboard-float-right">
            <a href="javascript:void(0)"  @click="logout">Logout</a>
        </div>
        <div class="dashboard-float-left">
            <template v-if="activeui === 'PROTOCOL_LOAD'">
                <a href="javascript:void(0)" class="symbol" @click="() => activeui = 'MAIN_MENU'">Zur&uuml;ck</a>
            </template>
            <template v-else-if="activeui === 'MAIN_MENU'">
                <a href="javascript:void(0)" @click="() => activeui = 'PROTOCOL_LOAD'">Laden</a>
            </template>
        </div>
    </div>

    <flash-messages></flash-messages>
    <loader v-if="activeui === 'LOADING'"></loader>
    <page-protocol
        v-else-if="activeui === 'MAIN_MENU'"
        v-model="protocol"
        :organizations="organizations"
        :facilities="facilities"
        :persons="persons"
        :categories="categories"
        :inspection-standards="inspectionStandards"
        @submit="submitProtocol">
    </page-protocol>
    <page-load
        v-else-if="activeui === 'PROTOCOL_LOAD'">
    </page-load>
  </div>
</template>

<script>
import FlashMessages from './FlashMessages'
import Loader from './Loader'

import PageProtocol from './PageProtocol'
import PageLoad from './PageLoad'

import { EventBus } from "../EventBus.js";
import { postProtocol, fetch } from '../ajax.js';
import { urlRender } from '../urls.js';

const $ = require('jquery');

export default {
    name: 'Main',
    components: {
        FlashMessages,
        Loader,
        PageProtocol,
        PageLoad,
    },
    data: function() {
        return {
            flashMessages: [],
            activeui: 'MAIN_MENU',
            protocol: {
                _id: null,
                header: this.newHeaderData(),
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
                this.protocol.header = this.newHeaderData();
                this.protocol.entries = [];
                this.protocol._id = null;

                this.renderProtocol(_id);
            }, () => {
                this.activeui = 'MAIN_MENU';
                EventBus.$emit('flash', { msg: 'Protokoll konnte nicht angelegt werden!', status: 'error' });
            });
        },
        logout: function() {
            console.log('That would be a nice feature, wouldn\'t it?');
        },
        newHeaderData: function() {
            return {
                title: '',
                inspectionStandards: '',
                facility: {
                    repr: '',
                    data: {
                        _id: null,
                    }
                },
                inspectionDate: '',
                inspector: {
                    repr: '',
                    data: {
                        _id: null,
                    }
                },
                issuer: {
                    repr: '',
                    data: {
                        _id: null,
                    }
                },
                attendees: ''
            };
        },
    }
}
</script>

<style>

div#dashboard {
    position: fixed;
    width: 100%;
    z-index: 9999;
    margin: 0px;
    top: 0;
    left: 0;
}

#dashboard {
    background: #303F9F;
    height: 63px;
    text-align: center;
}

#dashboard a {
    color: #E8EAF6;
    text-decoration: none;
    font-style: italic;
    font-size: 20px;
    font-weight: bold;
    padding: 9px;
    margin-left: 3px;
}

#dashboard a:hover {
    color: #303F9F;
    background: #E8EAF6;
}

.dashboard-float-right {
    float: right;
    margin-right: 5px;
    position: relative;
    top: 30%;
}

.dashboard-float-left {
    float: left;
    margin-left: 5px;
    position: relative;
    top: 30%;
}

</style>
