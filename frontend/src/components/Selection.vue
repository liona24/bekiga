<template>
    <drops-down :items="dropdownItems" @selected="selected">
        <div style="display: inline-block">
            <input 
                v-model="query"
                type="text"
                @focus="showDropdown = true"
                @mouseover="onMouseOver"
                @mouseout="showPreview = false"
                @blur="showDropdown = false"
                placeholder="Suche...">
            <div @click="clear" class="clear"><span>&times;</span></div>
        </div>
        <div v-if="showPreview" class="bubble">
            <slot name="preview">Keine Vorschau verf&uuml;gbar</slot>
        </div>
        <overlay :show="showCreateForm" @close="onCreateFormClosed">
            <slot>Nicht verf&uuml;gbar</slot>
        </overlay>
    </drops-down>
</template>

<script>

import DropsDown from './DropsDown'
import Overlay from './Overlay'

const _ = require('lodash');

export default {
    name: 'Selection',
    components: {
        DropsDown,
        Overlay
    },
    props: {
        items: Array,
        value: Object
    },
    data: function() {
        return {
            showDropdown: false,
            showCreateForm: false,
            showPreview: false,
            query: ''
        }
    },
    created: function() {
        if (this.value.repr === undefined) {
            this.setValue(this.getNew());
        } else {
            this.query = this.value.repr;
        }
    },
    watch: {
        value: function(newVal) {
            this.query = newVal.repr;
        }
    },
    computed: {
        dropdownItems: function() {
            if (!this.showDropdown) {
                return [];
            }

            let rv = this.items;
            if (this.query !== '') {
                rv = rv.filter((i) => i.repr.indexOf(this.query) >= 0);
            }

            return rv.concat({ repr: 'Neu ...', data: 'addnew' })
        }
    },
    methods: {
        selected: function(e) {
            this.showDropdown = false;
            if (e.data == 'addnew') {
                this.showCreateForm = true;
            } else {
                this.setValue(Object.assign({}, e));
            }
        },
        clear: function() {
            this.setValue(this.getNew());
            this.showDropdown = false;
        },
        onMouseOver: function() {
            if (this.value.data && this.value.data._id) {
                this.showPreview = true;
            }
        },
        onCreateFormClosed: function(e) {
            this.showCreateForm = false;
            if (e.success) {
                console.log('CREATED');
                console.log(e);
                this.setValue(Object.assign({}, e.data));
            }
        },
        getNew: function() {
            return { repr: '', data: { _id: null } };
        },
        setValue: function(v) {
            this.$emit('input', v);
        }
    }
}
</script>

<style scoped>

input[type=text] {
    float: left;
    width:379px; 
    height:27px; 
    line-height:27px;
    text-indent:10px; 
    font-family:arial, sans-serif; 
    font-size:1em; 
    color:#333; 
    background: #fff; 
    border:solid 1px #d9d9d9; 
    border-top:solid 1px #c0c0c0; 
    border-right:none;
}

div.clear {
    cursor: pointer;
    float: left;
    margin-top: 7px;
    margin-bottom: 7px;
}

.clear span {
    float:left; 
    width:16px;
    height:29px; 
    line-height:27px; 
    margin-right:15px; 
    padding:0 10px 0 10px;
    font-family: "Lucida Sans", "Lucida Sans Unicode", sans-serif;
    font-size:22px; 
    color: rgb(136, 136, 136);
    background: #fff;  
    border:solid 1px #d9d9d9; 
    border-top:solid 1px #c0c0c0; 
    border-left:none;
    -webkit-box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
    -moz-box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
    box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
}

.clear span:hover {
    color: #000;
}

</style>
