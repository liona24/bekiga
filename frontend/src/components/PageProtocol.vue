<template>
<div id="forms">
    <form-header id="protocol-header" v-model="protocol.header" :organizations="organizations" :persons="persons" :facilities="facilities"></form-header>
    <form-entry v-for="(entry, index) in protocol.entries" 
        :key="'entryform-' + index"
        :id="'entry-' + index"
        v-model="entry.data"
        :categories="categories"
        :inspection-standards="inspectionStandards"
        @delete="deleteEntry(index)">
    </form-entry>
    <div class="navigation-sidebar">
        <p>
            <a class="header-link" href="#protocol-header">{{ protocol.header.title }}</a>
        </p>
        <ul>
            <li v-for="(entry, idx) in protocol.entries" :key="'entrylink-' + idx">
                <a class="entry-link" :href="'#entry-' + idx">{{ entry.data.title ? entry.data.title : 'Eintrag ' + (idx + 1) }}</a>
            </li>
        </ul>
    </div>
    <input type="button" value="+" @click="addEntry" class="add-entry">
    <input type="button" value="Speichern" @click="submit" class="protocol-submit">
</div>

</template>

<script>
import FormEntry from './FormEntry'
import FormHeader from './FormHeader'

import { EventBus } from '../EventBus.js'

export default {
    name: 'PageProtocol',
    components: {
        FormHeader,
        FormEntry
    },
    props: {
        value: Object,

        organizations: Array,
        persons: Array,
        facilities: Array,
        categories: Array,
        inspectionStandards: Array,
    },
    created: function() {
        if (this.protocol.entries.length === 0) {
            this.addEntry();
        }
    },
    computed: {
        protocol: function() {
            return this.value;
        }
    },
    methods: {
        addEntry: function() {
            this.protocol.entries.push({ data: this.newEntryData() });
        },
        newEntryData: function() {
            return {
                category: {
                    repr: '',
                    data: {
                        _id: null,
                    }
                },
                flawInformation: [],
                title: '',
                manufacturer: '',
                yearBuilt: '', 
                inspectionSigns: '',
                manufactureInfoAvailable: 'Keine Angabe', 
                easyAccess: 'Keine Angabe',
            };
        },
        deleteEntry: function(index) {
            this.protocol.entries.splice(index, 1);
            EventBus.$emit('flash', { msg: 'Eintrag wurde gelöscht', status: 'okay' });
        },
        submit: function() {
            this.$emit('submit');
        }
    }
}
</script>


<style scoped>

input[type=button].add-entry {
    width: 65px;
    height: 65px;
    border-radius: 65px;
    bottom: 100px;
    position: fixed;
    bottom: 5%;
    right: 10%;
    font-size: 20px;
    font-weight: 500;
}

input[type="button"].protocol-submit {
    display: block;
    text-align: center;
    width: 800px;
    height: 40px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    margin-bottom: 10px;
    font-weight: bold;
}

div.navigation-sidebar {
    position: fixed;
    top: 20%;
    margin-left: 15px;
    border: 2px solid #303F9F;
    border-radius: 3px;
    text-align: center;
    max-height: 500px;
    overflow-y: auto;
}

.navigation-sidebar p {
    margin-left: 4px;
    margin-right: 4px;
}

a.header-link {
    font-size:1.2em; 
    font-style: normal;
    font-weight: bold;
    font-family:arial, sans-serif; 
    color:#303F9F; 
    text-decoration: none;
}
.navigation-sidebar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}
 
li {
  font: 200 1em Helvetica, Verdana, sans-serif;
  margin-bottom: 3px;
  text-align: center;
  padding: 5px;
}
 
a.entry-link {
  text-decoration: none;
  color: #000;
  display: block;
  width: 100%;
 
  -webkit-transition: font-size 0.2s ease, background-color 0.2s ease;
  -moz-transition: font-size 0.2s ease, background-color 0.2s ease;
  -o-transition: font-size 0.2s ease, background-color 0.2s ease;
  -ms-transition: font-size 0.2s ease, background-color 0.2s ease;
  transition: font-size 0.2s ease, background-color 0.2s ease;
}
 
a.entry-link:hover {
  font-size: 1.5em;
  background: #E8EAF6;
}
</style>
