
<template>
    <form>
        <input type="button" @click="$emit('delete')" value="X" class="btn-delete" style="left: 96%;" v-show="!locked">
        <fieldset>
            <legend align="top">
                <label>&#128274;
                    <input type="checkbox" v-model="locked">
                </label>
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
                        <input type="button" @click="removeFlawInfo(index)" class="btn-delete" value="X" v-show="!locked">
                    </legend>
                    <img :src="fi.pictureData" v-show="fi.pictureData">
                    <label>
                        <span>Mangel:</span> 
                        <autocomplete-input collection="flaws" mkey="flaw" v-model="fi.flaw" placeholder="Mangel" :disabled="locked"></autocomplete-input>
                    </label>
                    <label>
                        <span>Priorit&auml;t:</span>
                        <autocomplete-input collection="flaws" mkey="priority" v-model="fi.priority" placeholder="Priorität" :disabled="locked"/>
                    </label>
                    <label>
                        <span>Bemerkungen:</span>
                        <textarea v-model="fi.notes" placeholder="Bemerkungen" :disabled="locked"></textarea>
                    </label>
                    <label>
                        <span>Bild anf&uuml;gen:</span>
                        <input type="file" accept="image/*" v-on:change="handlePictureUpload($event, fi)" :disabled="locked">
                    </label>
                </fieldset>
            </div>
            <br>
            <input type="button" @click="addFlawInfo" style="float: right" value="+ Mangel" v-show="!locked">
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
    data: function() {
        return {
            props: '',
            newFlawInfo: {
            },
            locked: false
        };
    },
    created: function() {
        this.props = this.value.title !== undefined ? this.value : {
            category: {
                repr: '',
                data: {
                    _id: null,
                }
            },
            flawInformation: [],
            title: '',
            manufacturer: '',
            yearBuilt: '', 
            checkSign: '',
            manufactureInfoAvailable: 'Keine Angabe', 
            easyAccess: 'Keine Angabe',
        };
        if (this.props.flawInformation.length === 0) {
            this.props.flawInformation.push(this.newFlawInfoData());
        }
    },
    watch: {
        props: function() {
            this.$emit('input', this.props);
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
            /*
            let obj = {};
            if (this.newFlawInfo.flaw) {
                obj.flaw = this.newFlawInfo.flaw;
                this.newFlawInfo.flaw = '';
            }
            if (this.newFlawInfo.notes) {
                obj.notes = this.newFlawInfo.notes;
                this.newFlawInfo.notes = '';
            }
            if (this.newFlawInfo.priority) {
                obj.priority = this.newFlawInfo.priority;
                this.newFlawInfo.priority = '';
            }
            if (this.newFlawInfo.picture) {
                obj.pic = this.newflawInfo.picture;
                this.newFlawInfo.picture = '';

                // Reset input
                const inp = this.$refs.newPictureInput;
                inp.type = 'text';
                inp.type = 'file';
            }
            if (!obj) {
                return;
            }

            if (obj.pic) {
                let reader = new FileReader();
                let pic = obj.pic;
                obj.pic = '';
                reader.addEventListener('load', () => {
                    obj.pic = reader.result;
                }, false);
                reader.readAsDataURL(pic);
            }
            this.properties.flawInformation.push(obj);
            */
/*
            let formData = new FormData();
            formData.append('flaw', obj.flaw);
            formData.append('notes', obj.notes);
            formData.append('priority', obj.priority);
            formData.append('pic', obj.pic);

            $.ajax({
                url : 'http://localhost:5000/_uploads/flaws/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                type: 'POST',
                success: (data) => {
                    console.log(data);
                    let fi = {
                        _id: data.id,
                        $collection: 'flaw_information',
                        flaw: obj.flaw,
                        notes: obj.notes,
                        priority: obj.priority,
                        showPic: false,
                        readOnly: true,
                        pic: '' 
                    };
                    if (obj.pic) {
                        let reader = new FileReader();
                        reader.addEventListener('load', () => {
                            fi.showPic = true;
                            fi.pic = reader.result;
                        }, false);
                        reader.readAsDataURL(obj.pic);
                    }
                    this.flawInformation.push(fi);
                }
            });
            */
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