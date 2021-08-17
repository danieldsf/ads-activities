from browser import document, alert, window
from datetime import datetime
import math, json

global BASE_URL
global editId

jq = window.jQuery

haha = 'Foguinho'

editId = None

BASE_URL = 'http://localhost:5000/notes'

print(BASE_URL)

class Row():
	def __init__(self, id, name):
		self.name = name
		self.id = id
		self.deleteButton = '<button class="btn btn-danger delete" data-id="%s"><span class="glyphicon glyphicon-trash"></span>&nbsp;Deletar</button>' % self.id
		self.editButton = '<button class="btn btn-warning edit" data-id="%s"><span class="glyphicon glyphicon-pencil"></span>&nbsp;Editar</button>' % self.id

	def __str__(self):
		return '<tr><td>%s</td><td id="name_%s">%s</td><td>%s&nbsp;%s</td></tr>' % (self.id, self.id, self.name, self.editButton, self.deleteButton)

def fetchData(data, status, req):
	acumulator = ''

	for i in data.notes:
		row = Row(i.id, i.name)
		acumulator += str(row)
	
	if acumulator == '':
		acumulator = '<tr><td colspan="3">Lista de notas não presente</td></tr>'
	
	jq('#corpo').html(acumulator)

def onError(data, status, req):
	alert('Error')

def onSuccess(data, status, req):
    alert(data.message)
    consume()

def save(ev):
	nome = jq('#name').val()
   	jq.ajax({'url': BASE_URL,'type': 'POST' , 'data': {'name': nome},'success': onSuccess, 'error': onError})

def delete(ev):
	id = jq(ev.target).data('id')
	print(id)
	jq.ajax({'url': '%s/%s' % (BASE_URL, id), 'type': 'DELETE','success': onSuccess, 'error': onError})

def edit(ev):
	global editId
	
	editId = jq(ev.target).data('id')
	
	name = jq('#name_%s' % editId).text()

	jq('#name').val(name)	
	
	jq("#save").off()

	jq('#save').on('click', editCommit)

def editCommit(ev):
	global editId
	
	nome = jq('#name').val()
	
	jq.ajax({'url': '%s/%s' % (BASE_URL, editId),'type': 'PUT' , 'data': {'name': nome},'success': onSuccess, 'error': onError})
	
	editId = None
	
	jq('#name').val('')
	
	jq("#save").off()

	jq('#save').on('click', save)

def consume():
	jq.ajax({'url': BASE_URL,'type': 'GET' , 'success': fetchData, 'error': onError})

def revertString(ev):
	nome = jq('#name').val()
	
	nome = nome[::-1]
	
	jq('#name').val(nome)

def searchString(ev):
	nome = jq('#query').val().strip()
   	
   	if len(nome) > 0:
   		print(nome)
   		jq.ajax({'url': '%s/q/%s' % (BASE_URL, nome),'type': 'GET' , 'success': fetchData, 'error': onError})	
   	else:
   		consume()

jq('#save').on('click', save)

jq('#delete').on('click', delete)

jq('#revert').on('click', revertString)

jq('#query').on('keyup', searchString)

consume()

jq(document).on('click', '.delete', delete)

jq(document).on('click', '.edit', edit)

print(datetime.now())

print(json.dumps({'he':'HAHA'}))
