<template>
<div id="forms">
    <form-header v-model="protocol.header" :organizations="organizations" :persons="persons" :facilities="facilities"></form-header>
    <form-entry v-for="(entry, index) in protocol.entries" 
        :key="'entryform-' + index"
        v-model="entry.data"
        :categories="categories"
        :inspection-standards="inspectionStandards"
        @delete="deleteEntry(index)">
    </form-entry>
    <input type="button" value="+" @click="addEntry" class="add-entry">
</div>

</template>

<script>
import FormEntry from './FormEntry'
import FormHeader from './FormHeader'

import { EventBus } from '../EventBus.js'

export default {
    name: 'PageAdd',
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
    data: function() {
        return {
            protocol: {
                header: '',
                entries: []
            }
        }
    },
    watch: {
        protocol: function() {
            this.$emit('input', this.protocol);
        }
    },
    created: function() {
        this.protocol = this.value;
        if (this.protocol.header === undefined || this.protocol.header.title === undefined) {
            this.protocol.header = this.newHeaderData();
        }
        if (this.protocol.entries.length === 0) {
            this.addEntry();
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
                checkSign: '',
                manufactureInfoAvailable: 'Keine Angabe', 
                easyAccess: 'Keine Angabe',
            };
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
        deleteEntry: function(index) {
            this.protocol.entries.splice(index, 1);
            EventBus.$emit('flash', { msg: 'Eintrag wurde gelöscht', status: 'okay' });
        },
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

</style>
