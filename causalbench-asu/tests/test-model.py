from causalbench.modules import Model


model_web = Model(module_id=4, version=1)
model_path = model_web.fetch()
model1 = Model(zip_file=model_path)
#model1.publish(public=True)
assert model1.type=="model", "Model could not be fetched from web."

model2 = Model(zip_file='model/ges.zip')
#model2.publish(public=True)
assert model2.type=="model", "Local model could not be extracted."
