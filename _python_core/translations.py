from typing import Dict

sentences: Dict = {
    "en": {
        #
        "ERROR_DATA_DUPLICATED_IN_DB": "It exists in DB a {} with the same fields: {}",
        "ERROR_DATA_DUPLICATED_IN_FILE": "It exists in the uploaded file a {} with the same fields: {}",
        # BaseClass
        "ERROR_MISSING_ID": "Missing ID in data.",
        # Validations
        "ERROR_EMPTY_FILE": "File is Empty",
        "ERROR_EMPTY_DATA": "The entry was empty",
        "ERROR_MISSING_FIELD": "Field {} not provided",
        "ERROR_REQUIRED_FIELD": "The field {} is required",
        "ERROR_INVALID_VALUE_FOR_SPECIFIC_FIELD": "The value for the field {} is not correct",
        "ERROR_DELETE_NONEXISTING": "You can't delete non existing entity in database.{}",
        "ERROR_DATE_FORMAT": "Incorrect date format, should be YYYY-MM-DD. Check if day exists for month selected",
        "ERROR_ID_FIELD": "Incorrect data format for the field ID",
        # CheckDuplicate
        "ERROR_DUPLICATE_ALREADY_EXIST": "Error when inserting the entry because there already exists an entry with the same Field/Fields. {}",
        "ERROR_DUPLICATE_NON_EXISTING_FIELD": "Original entry:{} doesn't contain that field.{}",
        # IS_USED
        "ERROR_IS_ATTRIBUTE_USED": "Cannot perform the action. It is being used by {} collection.",
        # GetDifferences
        "ERROR_TYPE_MISMATCH": "Variable types do not match:{}",
        "ERROR_TYPE_FIELD": "Expected type: {} and {} was given for the field: {}",
        # CrudOptions
        "ERROR_WRONG_ACTION_CHANGELOG": "ChangeLog only admits: Create, Update or Delete",
        "ERROR_WRONG_DATE_FILTER": "You cannot send a request Date with minDate and maxDate, please send request Date, date range, minDate or maxDate",
        # Crud
        "ERROR_LIMIT_TOO_LOW": "The limit set to get_with_limit is too low. Limit:{}",
        "ERROR_EMPTY_SCHEMA": "Data is empty.",
        "ERROR_INVALID_ID": "The entry has an invalid ID.{}",
        "ERROR_UNKNOWN_MONGO_INSERT": "Something went wrong when inserting the entry in Mongo.{}",
        "ERROR_UNKNOWN_MONGO_UPDATE": "Something went wrong when editing the entry in Mongo.{}",
        "ERROR_UNKNOWN_MONGO_SOFT_DELETE": "Something went wrong when soft deleting the entry in Mongo.{}",
        "ERROR_UNKNOWN_MONGO_HARD_DELETE": "Something went wrong when hard deleting the entry in Mongo.{}",
        "MSG_SUCCESSFULLY_INSERTED": "The entry has successfully been inserted.{}",
        "MSG_SUCCESSFULLY_UPDATED": "The entry has successfully been updated.{}",
        "MSG_SUCCESSFULLY_SOFT_DELETED": "The entry has successfully been soft deleted.{}",
        "MSG_SUCCESSFULLY_HARD_DELETED": "The entry has successfully been hard deleted.{}",
        "ERROR_CRUDOPTIONS_LANGUAGE_DISCREPANCY": "The Options Language needs to be the same language than the Crud Object.",
        "ERROR_UNEXISTING_DATA": "This data doesn't exist in the database.",
        "ERROR_UNKNOWN_ACTION_CHANGELOG": "Unknown Action Changelog.{}",
        "MESSAGE_NO_CHANGES_TO_UPDATE": "This entry has no changes to update.{}",
    },
    "es": {
        "ERROR_DATA_DUPLICATED_IN_DB": "Ya existe en la BBDD un/una {} con los mismos campos: {}",
        "ERROR_DATA_DUPLICATED_IN_FILE": "Ya existe en el fichero que se subió un/una {} con los mismos campos: {}",
        # BaseClass
        "ERROR_MISSING_ID": "ID no encontrado en los datos.",
        # Validations
        "ERROR_EMPTY_FILE": "Fichero vacío.",
        "ERROR_EMPTY_DATA": "Datos vacíos.",
        "ERROR_MISSING_FIELD": "Campo {} no enviado",
        "ERROR_REQUIRED_FIELD": "El campo {} es obligatorio",
        "ERROR_INVALID_VALUE_FOR_SPECIFIC_FIELD": "El valor introducido para el campo {} no es válido",
        "ERROR_DELETE_NONEXISTING": "No puedes eliminar una entidad que no existe en la base de datos.{}",
        "ERROR_DATE_FORMAT": "Formato incorrecto para la fecha, debe usar: YYYY-MM-DD. Comprueba si el dia existe para el mes seleccionado",
        "ERROR_ID_FIELD": "Formato incorrecto para el campo ID",
        # CheckDuplicate
        "ERROR_DUPLICATE_ALREADY_EXIST": "Error al insertar la entrada porque ya existe una entrada con ese/esos mismo/s campo/s. {}",
        "ERROR_DUPLICATE_NON_EXISTING_FIELD": "La entrada original:{} no contiene ese campo.{}",
        # IS_USED
        "ERROR_IS_ATTRIBUTE_USED": "No se puede ejecutar esta acción. Esta siendo usado desde la colección {}.",
        # GetDifferences
        "ERROR_TYPE_MISMATCH": "Los tipos de las variables no concuerdan:{}",
        "ERROR_TYPE_FIELD": "Tipo esperado: {} y se ha proporcionado el tipo: {} para el campo: {}",
        # CrudOptions
        "ERROR_WRONG_ACTION_CHANGELOG": "ChangeLog sólo admite las siguientes opciones: Create, Update or Delete.",
        "ERROR_WRONG_DATE_FILTER": "No puede enviar una fecha de solicitud con minDate y maxDate, envíe la solicitud de fecha, rango de fechas, minDate o maxDate",
        # Crud
        "ERROR_LIMIT_TOO_LOW": "El límite para la función get_with_limit es demasiado pequeño. Límite:{}",
        "ERROR_EMPTY_SCHEMA": "Los datos están vacíos.",
        "ERROR_INVALID_ID": "La entrada tiene un ID inválido.{}",
        "ERROR_UNKNOWN_MONGO_INSERT": "Error inesperado al insertar la entrada en Mongo.{}",
        "ERROR_UNKNOWN_MONGO_UPDATE": "Error inesperado al editar la entrada en Mongo.{}",
        "ERROR_UNKNOWN_MONGO_SOFT_DELETE": "Error inesperado al eliminar en modo soft la entrada en Mongo.{}",
        "ERROR_UNKNOWN_MONGO_HARD_DELETE": "Error inesperado al eliminar en modo hard la entrada en Mongo.{}",
        "MSG_SUCCESSFULLY_INSERTED": "La entrada se ha insertado correctamente.{}",
        "MSG_SUCCESSFULLY_UPDATED": "La entrada se ha actualizado correctamente.{}",
        "MSG_SUCCESSFULLY_SOFT_DELETED": "La entrada se ha eliminado en modo soft de la base de datos.{}",
        "MSG_SUCCESSFULLY_HARD_DELETED": "La entrada se ha eliminado de la base de datos.{}",
        "ERROR_CRUDOPTIONS_LANGUAGE_DISCREPANCY": "El idioma de las opciones tiene que ser igual al idioma del Objeto Crud.",
        "ERROR_UNEXISTING_DATA": "Estos datos no existen en la base de datos.",
        "ERROR_UNKNOWN_ACTION_CHANGELOG": "Acción para changelog desconocida.{}",
        "MESSAGE_NO_CHANGES_TO_UPDATE": "Estos datos no tienen cambios para actualizar.{}",
    },
}


class Translations:
    def __init__(self, commonTranslations: Dict, serviceTranslation: Dict):
        self.commonTranslations = commonTranslations
        self.serviceTranslation = serviceTranslation

    def merge(self) -> None:
        for lang in set(self.commonTranslations).intersection(self.serviceTranslation):
            self.commonTranslations[lang].update(self.serviceTranslation.get(lang))
        for lang in set(self.serviceTranslation).difference((set(self.commonTranslations))):
            self.commonTranslations[lang] = self.serviceTranslation[lang]

    def get(self) -> Dict:
        return self.commonTranslations

    @staticmethod
    def translate(msg: str, lang: str = "en") -> str:
        lang = "en" if lang not in sentences.keys() else lang
        return sentences[lang].get(msg, msg)


def merge(commonDict: Dict, serviceDict: Dict) -> Dict:
    translations = Translations(commonDict, serviceDict)
    translations.merge()
    return translations.get()
