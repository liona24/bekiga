
<template>
    <drops-down :items="dropdownItems" @selected="selected">
        <textarea :placeholder="placeholder"
            @input="onInput($event.target.value)"
            @blur="clearSuggestions()"
            @keydown.esc="clearSuggestions()"
            v-model="query"></textarea>
    </drops-down>
</template>

<script>

import DropsDown from './DropsDown';
import { urlSuggest } from '../urls.js';

const _ = require('lodash');
const $ = require('jquery');

export default {
    name: 'AutocompleteTextarea',
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
        }
    },
    computed: {
        query: {
            get: function() {
                return this.value;
            },
            set: function(v) {
                this.$emit('input', v);
            }
        }
    },
    methods: {
        onInput: function(value) {
            if (!!value) {
                this.fetchSuggestions();
            }
        },
        selected: function(e) {
            this.query = e.repr;
            this.clearSuggestions();
        },
        clearSuggestions: function() {
            this.dropdownItems = [];
        },
        fetchSuggestions: _.debounce( function() {
            let data = {
                collection: this.collection,
                on: this.mkey,
                q: this.query,
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
        }, 200),
    }
}
</script>

<style scoped>

</style>
