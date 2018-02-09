<template>
    <form>
        <fieldset>
            <legend align="top">
                Firma
            </legend>

            <label>Name: 
                <CInput v-model="properties.name" :suggestConfig="suggestConfigs.name" placeholder="Name" type="text" />
            </label>
            <label>Straße/Hausnummer: 
                <CInput v-model="properties.street" :suggestConfig="suggestConfigs.street" placeholder="Straße/Hausnummer" type="text" />
            </label>
            <label>Postleitzahl: 
                <CInput v-model="properties.zipCode" :suggestConfig="suggestConfigs.zipCode" placeholder="Postleitzahl" type="text" />
            </label>
            <label>Stadt: 
                <CInput v-model="properties.city" :suggestConfig="suggestConfigs.city" placeholder="Stadt" type="text" />
            </label>
            <br>
            <input type="button" @click="submit" style="float: right" value="Speichern">
        </fieldset>
    </form>
</template>

<script>

import CInput from './CInput'
const $ = require('jquery');

export default {
    name: 'FormCompany',
    components: {
        CInput
    },
    props: {
        name: {
            default: ''
        }
    },
    data: function() {
        return {
            properties: {
                name: {
                    value: '',
                    id: null
                },
                street: {
                    value: '',
                    id: null
                }, 
                zipCode: {
                    value: '',
                    id: null
                },
                city: {
                    value: '',
                    id: null
                }
            },
            suggestConfigs: {}
        };
    },
    created: function() {
        this.properties.name.value = this.name;
    },
    methods: {
        submit: function(e) {
            if (this.properties.name.value.length === 0) {
                alert('Name benötigt!');
                return;
            }
            $(e.target).prop('disabled', true);

            let data = {
                collection: 'companies',
                data: {
                    name: this.properties.name.value,
                    street: this.properties.street.value,
                    zip_code: this.properties.zipCode.value,
                    city: this.properties.city.value,
                }
            };
            $.ajax({
                type: 'POST',
                url : 'http://localhost:5000/_data/',
                data : JSON.stringify(data, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: (result, status) => {
                    this.$emit('submit', {
                        id: result.id,
                        value: this.properties.name.value
                    });
                }
            });
        }
    }
}
</script>

<style>

</style>
