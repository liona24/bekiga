<template>
    <form>
        <fieldset>
            <legend align="top">
                Objekt/Einrichtung
            </legend>
            <img :src="pictureData" v-show="pictureData">
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
            <label>
                <span>Bild anf&uuml;gen:</span>
                <input type="file" accept="image/*" v-on:change="handlePictureUpload">
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
    name: 'FormFacility',
    components: {
    },
    props: {
        name: {
            default: ''
        }
    },
    data: function() {
        return {
            props: {
                name: '',
                street: '',
                zipCode: '',
                city: '',
                picture: '',
            },
            pictureData: ''
        };
    },
    created: function() {
        this.props.name = this.name;
    },
    methods: {
        handlePictureUpload: function(e) {
            let file = e.target.files[0];
            this.props.picture = file;
            let reader = new FileReader();
            reader.addEventListener('load', () => {
                this.pictureData = reader.result;
                this.$emit('imageLoaded', reader.result);
            }, false);
            reader.readAsDataURL(file);
        },
        submit: function(e) {
            if (this.props.name.length === 0) {
                alert('Name benötigt!');
                return;
            }
            $(e.target).prop('disabled', true);

            let pictureType = this.props.picture ? this.props.picture.name.split('.').pop() : '';

            let formData = new FormData();
            formData.append('name', this.props.name);
            formData.append('zipCode', this.props.zipCode);
            formData.append('street', this.props.street);
            formData.append('city', this.props.city);
            formData.append('picture', pictureType);

            $.ajax({
                url : urlApi + 'facilities/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (resp) => {
                    console.log('FACILITY CREATED');
                    console.log(resp);
                    let _id = resp.result._id;

                    let newItem = { 
                        repr: this.props.name,
                        data: Object.assign({ _id: _id }, Object(this.props)),
                    };

                    EventBus.$emit('newFacilityAdded', newItem);

                    if (pictureType) {
                        let formData = new FormData();
                        formData.append('pic', this.props.picture);
                        formData.append('_id', 'facility_' + _id + '.' + pictureType);
                        $.ajax({
                            url : urlApi + 'files/',
                            data: formData,
                            contentType: false,
                            cache: false,
                            processData: false,
                            type: 'POST'
                        });
                    }

                    EventBus.$emit('flash', { msg: 'Einrichtung wurde hinzugefügt!', status: 'okay' });
                    this.$parent.$emit('close', { success: true, data: newItem });
                },
                error: () => {
                    EventBus.$emit('flash', { msg: 'Fehler! Einrichtung konnte nicht erstellt werden!', status: 'error' });
                    this.$parent.$emit('close', { success: false });
                }
            });
        }
    }
}
</script>

<style scoped>
img {
    width: 150px;
    height: auto;
    float: right;
}
</style>
