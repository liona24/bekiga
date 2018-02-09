<template>
    <form>
        <fieldset>
            <legend align="top">
            Organisation
            </legend>
            <label>
                <span>Name:</span> 
                <input type="text" placeholder="Name" v-model="props.name">
            </label>
            <label>
                <span>Straße/Hausnummer:</span> 
                <input type="text" placeholder="Straße" v-model="props.street">
            </label>
            <label>
                <span>Postleitzahl:</span> 
                <input type="text" placeholder="Postleitzahl" v-model="props.zipCode">
            </label>
            <label>
                <span>Stadt:</span> 
                <input type="text" placeholder="Stadt" v-model="props.city">
            </label>
            <br>
            <input type="button" @click="submit" style="float: right" value="Speichern">
        </fieldset>
    </form>
</template>

<script>

import { EventBus } from '../EventBus.js'
const $ = require('jquery');

export default {
    name: 'FormOrganization',
    components: {
        Selection,
    },
    props: {
        name: {
            default: ''
        },
    },
    data: function() {
        return {
            props: {
                name: '',
                street: '',
                zipCode: '',
                city: '',
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
            formData.append('street', this.props.street);
            formData.append('city', this.props.city);
            formData.append('zipCode', this.props.zipCode);

            $.ajax({
                url : 'http://localhost:5000/organizations/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (resp) => {
                    console.log('ORGANIZATION CREATED');
                    console.log(resp);

                    EventBus.$emit('newOrganizationAdded', { data: Object.assign({ _id: result.id }, Object(this.props)) })
                    this.$emit('close', { success: true });
                }
            });
        }
    }
}
</script>

<style>
</style>
