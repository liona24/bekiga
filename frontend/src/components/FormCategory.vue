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

            <ul>
                <li v-for="(std, idx) in props.inspectionStandards" :key="'inspectionStandard' + idx">
                    {{ std.repr }}
                </li>
            </ul>
                
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
import apiUrl from '../apiUrl.js'

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
                data: { dasd: 'asdasd' }
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
                url : apiUrl + 'categories/',
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
                    this.$parent.$emit('close', { success: true });
                }
            });
        }
    }
}
</script>

<style scoped>
/* TODO style list */
</style>
