<template>
    <drops-down :items="dropdownItems" @selected="selected">
        <input type="text" v-model="ivalue" :placeholder="placeholder">
    </drops-down>
</template>

<script>

import DropsDown from './DropsDown';
import { urlSuggest } from '../urls.js';

const _ = require('lodash');
const $ = require('jquery');

export default {
    name: 'AutocompleteInput',
    components: {
        DropsDown
    },
    props: {
        value: String,
        collection: String,
        mkey: String,

        placeholder: {
            default: ''
        }
    },
    data: function() {
        return {
            dropdownItems: [],
            ivalue: '',
        }
    },
    watch: {
        ivalue: function() {
            this.$emit('input', this.ivalue);

            if (this.ivalue) {
                this.fetchSuggestions();
            }
        },
    },
    created: function() {
        this.ivalue = this.value;
    },
    methods: {
        selected: function(e) {
            this.clearSuggestions();
            this.ivalue = e.repr;
        },
        clearSuggestions: function() {
            this.dropdownItems = [];
        },
        fetchSuggestions: _.debounce( function() {
            if (this.ivalue.length <= 1) {
                return;
            }

            let data = {
                collection: this.collection,
                on: this.mkey,
                q: this.ivalue,
            };
            console.log('GET:')
            console.log(JSON.stringify(data));
            $.ajax({
                type: 'GET',
                url: urlSuggest,
                data: data,
                success: (resp, status) => {
                    console.log('RECIEVE');
                    console.log(JSON.stringify(resp));
                    this.dropdownItems = resp.data.map(function(i) {
                        return { repr: i }
                    });
                }
            });
        }, 500),
    }
}
</script>

<style scoped>

</style>
