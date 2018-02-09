<template>
    <form>
        <fieldset>
            <legend>
                <span>Protokoll</span><autocomplete-input collection="protocols" mkey="title" placeholder="Titel" v-model="props.title"></autocomplete-input>
            </legend>

            <div class="inspection-standards">
                <label>
                    <span>Pr&uuml;fgrundlagen:</span>
                    <autocomplete-textarea collection="protocols" mkey="inspectionStandards" placeholder="Prüfgrundlagen" v-model="props.inspectionStandards"></autocomplete-textarea>
                </label>
            </div>

            <div class="header-body">
                <label>
                    <span>Objekt:</span>
                    <selection v-model="props.facility" :items="facilities">
                        <form-facility></form-facility>
                    </selection>
                </label>

                <label>
                    <span>Pr&uuml;fdatum:</span>
                    <input type="date" v-model="props.inspectionDate">
                </label>

                <label>
                    <span>Pr&uuml;fer:</span>
                    <selection v-model="props.inspector" :items="persons">
                        <form-person :organizations="organizations"></form-person>
                    </selection>
                </label>

                <label>
                    <span>Auftraggeber:</span>
                    <selection v-model="props.issuer" :items="organizations">
                        <form-organization></form-organization>
                    </selection>
                </label>

                <label>
                    <span>Weitere Teilnehmer:</span>
                    <input type="text" v-model="props.attendees" plaaceholder="Weitere Teilnehmer">
                </label>
            </div>
        </fieldset>
    </form>
</template>

<script>
import FormFacility from './FormFacility'
import FormPerson from './FormPerson'
import FormOrganization from './FormOrganization'

import AutocompleteInput from './AutocompleteInput'
import AutocompleteTextarea from './AutocompleteTextarea'
import Selection from './Selection'

export default {
    name: 'FormHeader',
    components: {
        AutocompleteInput,
        AutocompleteTextarea,
        Selection,

        FormFacility,
        FormPerson,
        FormOrganization,
    },
    props: {
        value: Object,

        organizations: Array,
        persons: Array,
        facilities: Array,
    },
    data: function() {
        return {
            props: '' 
        };
    },
    watch: {
        props: function() {
            this.$emit('input', this.props);
        }
    },
    created: function() {
        this.props = this.value.title !== undefined ? this.value : {
            title: '',
            inspectionStandards: '',
            inspectionDate: '',
            attendees: '',
            facility: {
                repr: '',
                data: {
                    _id: ''
                }
            },
            inspector: {
                repr: '',
                data: {
                    _id: ''
                }
            },
            issuer: {
                repr: '',
                data: {
                    _id: ''
                }
            }
        };
    },
}
</script>

<style scoped>

legend > * {
    margin-left: 10px;
}

</style>
