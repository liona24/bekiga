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
import { urlApi } from '../urls.js'

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
                url : urlApi + 'organizations/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (resp) => {
                    console.log('ORGANIZATION CREATED');
                    console.log(resp);

                    let _id = resp.result._id;
                    let newItem = {
                        data: Object.assign({ _id: _id }, Object(this.props)),
                        repr: this.props.name
                    };

                    EventBus.$emit('newOrganizationAdded', newItem);
                    EventBus.$emit('flash', { msg: 'Organisation wurde hinzugefügt!', status: 'okay' });
                    this.$parent.$emit('close', { success: true, data: newItem });
                },
                error: () => {
                    EventBus.$emit('flash', { msg: 'Fehler! Organisation konnte nicht erstellt werden!', status: 'error' });
                    this.$parent.$emit('close', { success: false });
                }
            });
        }
    }
}
</script>

<style>
</style>
