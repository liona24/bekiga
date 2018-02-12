<template>
    <form>
        <fieldset>
            <legend align="top">
                Person 
            </legend>
            <label>
                <span>Name:</span> 
                <input type="text" placeholder="Name" v-model="props.name">
            </label>
            <label>
                <span>Vorname:</span> 
                <input type="text" placeholder="Vorname" v-model="props.firstName">
            </label>
            <label>
                <span>E-Mail:</span> 
                <input type="email" placeholder="E-Mail" v-model="props.email">
            </label>
            <label>
                <span>Organisation:</span> 
                <selection :items="organizations" v-model="props.organization">
                    <form-organization></form-organization>
                </selection>
            </label>
            <br>
            <input type="button" @click="submit" style="float: right" value="Speichern">
        </fieldset>
    </form>
</template>

<script>

import FormOrganization from './FormOrganization'
import Selection from './Selection'

import { EventBus } from '../EventBus.js'
import { urlApi } from '../urls.js'

const $ = require('jquery');

export default {
    name: 'FormFacility',
    components: {
        Selection,
        FormOrganization,
    },
    props: {
        name: {
            default: ''
        },
        organizations: Array,
    },
    data: function() {
        return {
            props: {
                name: '',
                firstName: '',
                email: '',
                organization: {
                    repr: '',
                    data: { id: null },
                }
            },
        };
    },
    created: function() {
        this.props.name = this.name;
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
            formData.append('firstName', this.props.firstName);
            formData.append('email', this.props.email);
            formData.append('organization', this.props.organization.data._id);

            $.ajax({
                url : urlApi + 'persons/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (resp) => {
                    console.log('PERSON CREATED');
                    console.log(resp);

                    let _id = resp.result._id;
                    let newItem = {
                        data: Object.assign({ _id: _id }, Object(this.props)),
                        repr: this.props.name + ', ' + this.props.firstName
                    };

                    EventBus.$emit('newPersonAdded', newItem);
                    this.$parent.$emit('close', { success: true, data: newItem });
                }
            });
        }
    }
}
</script>

<style>
</style>
