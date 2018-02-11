<template>
    <drops-down :items="dropdownItems" @selected="selected">
        <textarea v-model="ivalue" :placeholder="placeholder"></textarea>
    </drops-down>
</template>

<script>

import DropsDown from './DropsDown';

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
            this.dropdownItems = [];
            this.ivalue = e.text;
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
                url: 'http://localhost:5000/_suggestions/',
                data: data,
                success: (resp, status) => {
                    console.log('RECIEVE');
                    console.log(JSON.stringify(resp));
                    this.dropdownItems = resp.data.map((i) => { text: i });
                }
            });
        }, 500),
    }
}
</script>

<style scoped>

</style>
