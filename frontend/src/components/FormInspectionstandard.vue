<template>
    <form>
        <fieldset>
            <legend align="top">
                Pr&uuml;fkriterium 
            </legend>
            <label>
                <span>Name:</span> 
                <input type="text" placeholder="Name" v-model="props.name">
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
    name: 'FormInspectionstandard',
    components: {
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

            $.ajax({
                url : urlApi + 'inspectionStandards/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (resp) => {
                    console.log('INSPECTION_STANDARD CREATED');
                    console.log(resp);

                    let _id = resp.result._id;
                    let newItem = {
                        data: Object.assign({ _id: _id }, Object(this.props)),
                        repr: this.props.name
                    };

                    EventBus.$emit('newInspectionStandardAdded', newItem);
                    EventBus.$emit('flash', { msg: 'Prüfgrundlage wurde hinzugefügt!', status: 'okay' });
                    this.$parent.$emit('close', { success: true, data: newItem });
                },
                error: () => {
                    EventBus.$emit('flash', { msg: 'Fehler! Prüfgrundlage konnte nicht erstellt werden!', status: 'error' });
                    this.$parent.$emit('close', { success: false });
                }
            });
        }
    }
}
</script>

<style>
</style>

