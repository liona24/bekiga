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
                        <preview-facility slot="preview" :data="props.facility.data"></preview-facility>
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
                        <preview-person slot="preview" :data="props.inspector.data"></preview-person>
                    </selection>
                </label>

                <label>
                    <span>Auftraggeber:</span>
                    <selection v-model="props.issuer" :items="organizations">
                        <form-organization></form-organization>
                        <preview-organization slot="preview" :data="props.issuer.data"></preview-organization>
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

import PreviewPerson from './PreviewPerson'
import PreviewOrganization from './PreviewOrganization'
import PreviewFacility from './PreviewFacility'

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

        PreviewPerson,
        PreviewOrganization,
        PreviewFacility,
    },
    props: {
        value: Object,

        organizations: Array,
        persons: Array,
        facilities: Array,
    },
    computed: {
        props: function() {
            return this.value;
        }
    },
}
</script>

<style scoped>

legend > * {
    margin-left: 10px;
}

</style>
