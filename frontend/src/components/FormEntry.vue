
<template>
    <form>
        <input type="button" @click="$emit('delete')" value="X" class="btn-delete" style="left: 96%;">
        <fieldset>
            <legend>
                Eintrag
            </legend>

            <div class="category">
                <selection v-model="props.category" :items="categories">
                    <form-category :inspection-standards="inspectionStandards"></form-category>
                </selection>
            </div>
            <label>
                <span>Bezeichung:</span> 
                <autocomplete-input collection="entries" mkey="title" placeholder="Bezeichnung" v-model="props.title"></autocomplete-input>
            </label>
            <label>
                <span>Hersteller:</span>
                <autocomplete-input collection="entries" mkey="manufacturer" placeholder="Hersteller" v-model="props.manufacturer"></autocomplete-input>
            </label>
            <label>
                <span>Baujahr:</span>
                <input type="number" size=4 placeholder="Baujahr" v-model="props.yearBuilt">
            </label>
            <label>
                <span>Pr&uuml;fzeichen:</span>
                <autocomplete-input collection="entries" mkey="inspectionSigns" placeholder="Prüfzeichen" v-model="props.inspectionSigns"></autocomplete-input>
            </label>
            <label>
                <span>Herstellerinformation:</span>
                <select v-model="props.manufactureInfoAvailable">
                    <option>Keine Angabe</option>
                    <option>Ja</option>
                    <option>Nein</option>
                </select>
            </label>
            <label>
                <span>Leicht zug&auml;nglich:</span>
                <select v-model="props.easyAccess">
                    <option>Keine Angabe</option>
                    <option>Ja</option>
                    <option>Nein</option>
                </select>
            </label>
            <div v-for="(fi, index) in props.flawInformation" :key="'flaw-' + index">
                <br>
                <fieldset>
                    <legend align="right">
                        <input type="button" @click="removeFlawInfo(index)" class="btn-delete" value="X">
                    </legend>
                    <img :src="fi.pictureData" v-show="fi.pictureData">
                    <label>
                        <span>Mangel:</span> 
                        <autocomplete-input collection="flaws" mkey="flaw" v-model="fi.flaw" placeholder="Mangel"></autocomplete-input>
                    </label>
                    <label>
                        <span>Priorit&auml;t:</span>
                        <autocomplete-input collection="flaws" mkey="priority" v-model="fi.priority" placeholder="Priorität"/>
                    </label>
                    <label>
                        <span>Bemerkungen:</span>
                        <textarea v-model="fi.notes" placeholder="Bemerkungen"></textarea>
                    </label>
                    <label>
                        <span>Bild anf&uuml;gen:</span>
                        <input type="file" accept="image/*" v-on:change="handlePictureUpload($event, fi)">
                    </label>
                </fieldset>
            </div>
            <br>
            <input type="button" @click="addFlawInfo" style="float: right" value="+ Mangel">
        </fieldset>
    </form>
</template>

<script>
import AutocompleteInput from './AutocompleteInput'
import Selection from './Selection'
import { EventBus } from '../EventBus.js'

import FormCategory from './FormCategory'

const $ = require('jquery');

export default {
    name: 'FormEntry',
    components: {
        AutocompleteInput,
        Selection,
        FormCategory,
    },
    props: {
        value: Object,
        categories: Array,
        inspectionStandards: Array
    },
    computed: {
        props: function() {
            return this.value;
        }
    },
    created: function() {
        if (this.props.flawInformation.length === 0) {
            this.props.flawInformation.push(this.newFlawInfoData());
        }
    },
    methods: {
        handlePictureUpload: function(e, flawInfo) {
            flawInfo.pictureFile = e.target.files[0];
            let reader = new FileReader();
            reader.addEventListener('load', () => {
                flawInfo.pictureData = reader.result;
            }, false);
            reader.readAsDataURL(flawInfo.pictureFile);
        },
        newFlawInfoData: function() {
            return {
                flaw: '',
                notes: '',
                priority: '',
                pictureFile: '',
                pictureData: ''
            };
        },
        removeFlawInfo: function(index) {
            this.props.flawInformation.splice(index, 1);
            EventBus.$emit('flash', { msg: 'Mangel wurde entfernt.', status: 'okay' });
        },
        addFlawInfo: function() {
            this.props.flawInformation.push(this.newFlawInfoData());
        }
    }
}
</script>

<style scoped>

.category {
    width: 100%;
    display: inline-block;
}

.category > div {
    float: right;
}


img {
    width: 150px;
    height: auto;
    float: right;
}
</style>