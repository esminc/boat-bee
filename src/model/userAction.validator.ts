// @ts-nocheck
// eslint-disable
// This file is generated by create-validator-ts
import Ajv from 'ajv';
import * as apiTypes from './userAction';

export const SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$ref": "#/definitions/UserAction",
    "definitions": {
        "UserAction": {
            "type": "object",
            "properties": {
                "userId": {
                    "type": "string"
                },
                "createdAt": {
                    "type": "string"
                },
                "actionName": {
                    "type": "string"
                },
                "status": {
                    "type": "string"
                },
                "payload": {}
            },
            "required": [
                "userId",
                "createdAt",
                "actionName",
                "status"
            ],
            "additionalProperties": false,
            "description": "ユーザの行動履歴"
        }
    }
};
const ajv = new Ajv({ removeAdditional: true }).addSchema(SCHEMA, "SCHEMA");
export function validateUserAction(payload: unknown): apiTypes.UserAction {
  /** Schema is defined in {@link SCHEMA.definitions.UserAction } **/
  const validator = ajv.getSchema("SCHEMA#/definitions/UserAction");
  const valid = validator(payload);
  if (!valid) {
    const error = new Error('Invalid UserAction: ' + ajv.errorsText(validator.errors, {dataVar: "UserAction"}));
    error.name = "ValidationError";
    throw error;
  }
  return payload;
}

export function isUserAction(payload: unknown): payload is apiTypes.UserAction {
  try {
    validateUserAction(payload);
    return true;
  } catch (error) {
    return false;
  }
}
