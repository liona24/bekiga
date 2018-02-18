<template>
    <form>
        <fieldset>
            <legend>
                Kategorie
            </legend>
            <label>
                <span>Name:</span> 
                <input type="text" placeholder="Name" v-model="props.name">
            </label>

            <div class="list">
                <label v-for="(std, idx) in props.inspectionStandards" :key="'inspectionStandard' + idx">
                    <span></span>
                    <div style="display: inline-block">
                        <input type="text" :value="std.repr" class="selected-item" disabled>
                        <div @click="remove(idx)" class="clear"><span>&times;</span></div>
                    </div>
                </label>
            </div>
                
            <label>
                <span>Pr&uuml;fkriterium aufnehmen:</span>
                <selection v-model="newInspectionStandard" :items="inspectionStandards">
                    <form-inspectionstandard></form-inspectionstandard>
                </selection>
            </label>
            <br>
            <input type="button" @click="submit" style="float: right" value="Speichern">
        </fieldset>
    </form>
</template>

<script>
import Selection from './Selection'
import FormInspectionstandard from './FormInspectionstandard'

import { EventBus } from '../EventBus.js'
import { urlApi } from '../urls.js'

const $ = require('jquery');

export default {
    name: 'FormCategory',
    components: {
        Selection,
        FormInspectionstandard
    },
    props: {
        name: {
            default: ''
        },
        inspectionStandards: Array
    },
    data: function() {
        return {
            props: {
                name: '',
                inspectionStandards: [],
            },
            newInspectionStandard: {
                repr: '',
                data: { _id: null }
            }
        };
    },
    created: function() {
        this.props.name = this.name;
    },
    watch: {
        newInspectionStandard: function(newVal) {
            if (newVal.data !== undefined && newVal.data._id !== undefined) {
                this.props.inspectionStandards.push(Object.assign({}, newVal));
                this.newInspectionStandard.repr = '';
                this.newInspectionStandard.data = null;
            }
        }
    },
    methods: {
        remove: function(idx) {
            this.props.inspectionStandards.splice(idx, 1);
        },
        submit: function(e) {
            if (this.props.name.length === 0) {
                alert('Name benötigt!');
                return;
            }
            $(e.target).prop('disabled', true);

            let formData = new FormData();
            formData.append('name', this.props.name);
            formData.append('inspectionStandards', this.props.inspectionStandards.map((i) => i.data._id));

            $.ajax({
                url : urlApi + 'categories/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (resp) => {
                    console.log('CATEGORY CREATED');
                    console.log(resp);

                    let id = resp.result._id;

                    let newItem = { 
                        data: Object.assign({ _id: id }, Object(this.props)),
                        repr: this.props.name
                    };

                    EventBus.$emit('newCategoryAdded', newItem);
                    EventBus.$emit('flash', { msg: 'Kategorie wurde hinzugefügt!', status: 'okay' });
                    this.$parent.$emit('close', { success: true, data: newItem });
                },
                error: () => {
                    EventBus.$emit('flash', { msg: 'Fehler! Kategorie konnte nicht erstellt werden!', status: 'error' });
                    this.$parent.$emit('close', { success: false });
                }
            });
        }
    }
}
</script>

<style scoped>

.selected-item {
    float: left;
    width: 377px;
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
