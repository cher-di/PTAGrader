MAIN_CONFIG_SCHEMA = {
    'type': 'object',
    'properties': {
        'grader': {
            'type': 'object',
            'properties': {
                'parallel': {'type': 'boolean'},
                'nogui': {'type': 'boolean'},
            }
        },
        'classroom': {
            'type': 'object',
            'properties': {
                'course_id': {'type': 'string'}
            }
        },
        'mailer': {
            'type': 'object',
            'properties': {
                'enable_students_mailing': {'type': 'boolean'},
                'enable_admins_mailing': {'type': 'boolean'},
                'server': {'type': 'string', 'format': 'hostname'},
                'connection': {'type': 'string', 'enum': ['ssl', 'tls']},
                'port': {'type': 'integer', 'minimum': 1, 'maximum': 65535},
                'address': {'type': 'string', 'format': 'email'},
                'password': {'type': 'string'},
                'admins_mail_list': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'format': 'email'
                    }
                }
            }
        }
    }
}

LABS_CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': {
        'type': 'object',
        'additionalProperties': {
            'type': 'object',
            'properties': {
                'filename': {'type': 'string'},
                'password': {'type': 'string'}
            }
        }
    }
}
