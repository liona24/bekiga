export function getRepr(obj, type) {
    switch (type) {
    case 'organization':
    case 'facility':
    case 'inspectionStandard':
    case 'category':
        return obj.name;
    case 'person':
        return obj.name + ', ' + obj.firstName;
    case 'protocol':
    case 'entry':
        return obj.title;
    case 'flaw':
        return obj.flaw;
    default:
        return 'ERROR: ' + JSON.stringify(obj) + ' of type "' + type + '"';
    }
}

export function endpointByType(type) {
    switch (type) {
        case 'organization':
            return 'organizations/';
        case 'entry':
            return 'entries/';
        case 'protocol':
            return 'protocols/';
        case 'person':
            return 'persons/';
        case 'category':
            return 'categories/';
        case 'facility':
            return 'facilities/';
        case 'inspectionStandard':
            return 'inspectionStandards/';
        case 'flaw':
            return 'flaws/';
    }
}